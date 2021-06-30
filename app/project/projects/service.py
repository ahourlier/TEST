import logging
import operator
import os
from datetime import date
from typing import List

import requests
from flask import request, g, current_app
from flask_sqlalchemy import Pagination
from sqlalchemy import or_, and_

import app.mission.missions.service as mission_service
import app.auth.users.service as user_service
import app.project.requesters.service as requester_service
import app.project.project_leads.service as project_lead_service

from app import db
from app.auth.users import User
from app.auth.users.model import UserRole
from app.common.anonymization_utils import (
    PROJECT_ANONYMIZATION_MAP,
    REQUESTER_ANONYMIZATION_MAP,
    ACCOMMODATION_ANONYMIZATION_MAP,
    CONTACT_ANONYMIZATION_MAP,
    PHONE_NUMBER_ANONYMIZATION_MAP,
)
from app.common.config_error_messages import (
    KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION,
    KEY_SHARED_DRIVE_COPY_EXCEPTION,
    KEY_SHARED_DRIVE_RENAME_EXCEPTION,
)
from app.common.constants import DATETIME_FORMAT
from app.common.drive_utils import DriveUtils, DRIVE_DEFAULT_FIELDS
from app.common.exceptions import (
    InconsistentUpdateIdException,
    SharedDriveException,
    InvalidSearchFieldException,
)
from app.common.google_apis import DriveService
from app.common.search import sort_query
from app.common.sheets_util import SheetsUtils
from app.common.tasks import create_task
from app.mission.teams.model import UserTeamPositions
from app.mission.missions import Mission
from app.mission.teams import Team
from app.project.permissions import ProjectPermission
from app.project.project_custom_fields.model import ProjectCustomField
from app.project.project_leads.model import ProjectLead

from app.project.projects import Project, api
from app.project.projects.error_handlers import ProjectNotFoundException
from app.project.projects.interface import ProjectInterface
from app.project.projects.model import ProjectDateStatus, ProjectStatus
from app.project.requesters import Requester
import app.project.comments.service as comment_service
import app.project.accommodations.service as accommodations_service
import app.common.anonymization_utils as anonymization_utils


import app.project.work_types.service as work_type_service
from app.project.requesters.model import RequesterTypes
from app.project.search.model import FORBIDDEN_FIELDS

PROJECTS_DEFAULT_PAGE = 1
PROJECTS_DEFAULT_PAGE_SIZE = 20
PROJECTS_DEFAULT_SORT_FIELD = "created_at"
PROJECTS_DEFAULT_SORT_DIRECTION = "desc"

PROJECT_INIT_QUEUE_NAME = "project-queue"
PROJECT_DELETE_DOCS_QUEUE_NAME = "project-delete-docs-queue"

SD_PROJECT_QUOTES_FOLDER_NAME = "Devis et Factures"
SD_PROJECT_ACCOMMODATION_FOLDER_NAME = "Logement"
SD_PROJECT_FUNDERS_FOLDER_NAME = "Financeurs"
SD_PROJECT_REQUESTER_FOLDER_NAME = "Demandeur"
SD_PROJECT_ACCOMMODATION_REPORT_FOLDER_NAME = "Compte-Rendus"
SD_PROJECT_ACCOMMODATION_PICTURES_FOLDER_NAME = "Photos"
PROJECT_DELETE_SD_PREFIX = "ZZ - [ARCHIVE]"


class ProjectService:
    @staticmethod
    def get_all(
        page=PROJECTS_DEFAULT_PAGE,
        size=PROJECTS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=PROJECTS_DEFAULT_SORT_FIELD,
        direction=PROJECTS_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        requester_id=None,
        user=None,
        requester_type=None,
        unique_page=False,
        filter_on_visit_status=False,
        filter_on_referrer=False,
    ) -> Pagination:
        if sort_by == "requester_last_name":
            q = Project.query.join(Project.requester).order_by(
                Requester.last_name.asc()
                if direction == "asc"
                else Requester.last_name.desc()
            )
        else:
            q = sort_query(Project.query, sort_by, direction)
        # Apply filters by text field

        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Project.code_name.ilike(search_term),
                    Project.requester.has(Requester.last_name.ilike(search_term)),
                    Project.requester.has(Requester.first_name.ilike(search_term)),
                )
            )

        q = ProjectService.filter_query_project(
            user=user,
            q=q,
            missions_id=mission_id,
            requester_id=requester_id,
            requester_type=requester_type,
            filter_on_visit_status=filter_on_visit_status,
            filter_on_referrer=filter_on_referrer,
            remove_unauthorized=True,
        )

        q = q.filter(Project.status != "Sans suite")

        if unique_page:
            # Retrieve all projects in one unique page
            size = q.count()

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def filter_query_project(
        user=None,
        q=None,
        missions_id=None,
        requester_id=None,
        requester_type=None,
        project_status: List = None,
        project_status_to_skip: List = None,
        fetch_deactivated=False,
        filter_on_referrer=False,
        filter_on_visit_status=False,
        remove_unauthorized=True,
    ):
        """Filter a query on Project table by various parameters:"""
        if user is None:
            user = g.user

        if q is None:
            q = Project.query

        # Filter by missions_id
        if missions_id is not None:
            if not isinstance(missions_id, list):
                missions_id = [missions_id]
            q = q.filter(
                or_(
                    *[
                        Project.mission_id == mission_id
                        for mission_id in missions_id
                        if type(mission_id) == int
                    ]
                )
            )

        # Filter by requester_id
        if requester_id is not None:
            q = q.filter(Project.requester_id == requester_id)

        # Filter by requester_type
        if (
            requester_type is not None
            and requester_type not in RequesterTypes.__members__
        ):
            raise InvalidSearchFieldException()
        if requester_type is not None:
            q = q.filter(Project.requester.has(Requester.type == requester_type))
        # Filter by project status
        if project_status is not None:
            if not isinstance(project_status, list):
                project_status = [project_status]
            q = q.filter(
                or_(
                    *[
                        Project.status == value
                        for value in project_status
                        if type(value) == str
                    ]
                )
            )

        # Skip by project status
        if project_status_to_skip is not None:
            if not isinstance(project_status_to_skip, list):
                project_status_to_skip = [project_status_to_skip]
            q = q.filter(
                and_(
                    *[
                        Project.status != value
                        for value in project_status_to_skip
                        if type(value) == str
                    ]
                )
            )

        # Filter by referrers
        if filter_on_referrer and user is not None:
            q = q.filter(Project.project_leads.any(ProjectLead.user_id == user.id))

        if filter_on_visit_status:
            visits_status = [
                ProjectStatus.MEET_ADVICES_TO_PLAN.value,
                ProjectStatus.MEET_ADVICES_PLANNED.value,
                ProjectStatus.MEET_CONTROL_TO_PLAN.value,
                ProjectStatus.MEET_CONTROL_PLANNED.value,
            ]
            q = ProjectService.filter_query_project(q=q, project_status=visits_status)

        # Remove unauthorized projects for current user:
        if remove_unauthorized:
            q = ProjectPermission.query_project_remove_unauthorized(q, user)

        # Deactivated projects must not be retrieved
        if not fetch_deactivated:
            q = q.filter(Project.active == True)

        return q

    @staticmethod
    def get_by_id(project_id: int) -> Project:
        db_project = Project.query.get(project_id)

        if db_project is None:
            raise ProjectNotFoundException

        return db_project

    @staticmethod
    def create(new_attrs: dict) -> Project:
        """ Create a new project with linked mission, referrers, and requester """
        project_leads = None
        work_types = None
        # Check if project_leads exist and save them :
        if new_attrs.get("referrers"):
            project_leads = new_attrs.get("referrers")
        del new_attrs["referrers"]
        # Check if work_types exist and save them :
        if new_attrs.get("work_types"):
            work_types = new_attrs.get("work_types")
        del new_attrs["work_types"]

        # Check if provided mission exists
        mission_service.MissionService.get_by_id(new_attrs.get("mission_id"))
        # Create a new requester
        requester = requester_service.RequesterService.create(
            new_attrs.get("requester")
        )
        new_attrs["requester_id"] = requester.id
        # Create project
        del new_attrs["requester"]
        new_project = ProjectInterface(**new_attrs)
        project = Project(**new_project)
        ProjectService.update_dates_status(project.status, project)
        db.session.add(project)
        db.session.commit()
        # Create project_leads
        if project_leads:
            project_lead_service.ProjectLeadService.create_list(
                project.id, project_leads
            )
        # Create work_types :
        if work_types:
            work_type_service.WorkTypeService.create_list(work_types, project.id)
        if project.requester.type in [
            "PO",
            "TENANT",
            "SDC",
        ]:
            logging.info(f"Creating accommodation for project {project.id}")
            accommodations_service.AccommodationService.create({}, project.id)
        db.session.commit()
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=PROJECT_INIT_QUEUE_NAME,
            uri=f"{request.host_url}_internal/projects/init-drive",
            method="POST",
            payload={"project_id": project.id,},
        )

        return project

    @staticmethod
    def update(
        project: Project, changes: ProjectInterface, force_update: bool = False
    ) -> Project:
        if force_update or ProjectService.has_changed(project, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != project.id:
                raise InconsistentUpdateIdException()
            # Update requester
            requester = requester_service.RequesterService.get_by_id(
                changes["requester"]["id"]
            )
            requester_service.RequesterService.update(
                requester, changes.get("requester")
            )
            # Update referrers
            project_lead_service.ProjectLeadService.update_list(
                changes.get("referrers"), project.id
            )
            # Update work types
            work_type_service.WorkTypeService.update_list(
                changes.get("work_types"), project.id
            )
            del changes["work_types"]
            del changes["referrers"]
            del changes["requester"]
            old_status = project.status
            project.update(changes)
            new_status = project.status

            # If status have changed, a new automatic comment registration may be requested,
            # and some dates may be saved
            if new_status != old_status:
                comment_service.AutomaticCommentService.automatic_project_status_comment(
                    new_status, project
                )
                ProjectService.update_dates_status(new_status, project)
            db.session.commit()
        return project

    @staticmethod
    def has_changed(project: Project, changes: ProjectInterface) -> bool:
        for key, value in changes.items():
            if getattr(project, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(project_id: int) -> int:
        """A project is never truly deleted. It's deactivated instead"""
        project = Project.query.filter(Project.id == project_id).first()
        if not project:
            raise ProjectNotFoundException
        project.active = False
        db.session.commit()
        names = []
        if project.requester.last_name:
            names.append(project.requester.last_name)
        if project.requester.first_name:
            names.append(project.requester.first_name)

        name = f"{PROJECT_DELETE_SD_PREFIX} {' '.join(names)} - {project.id}"
        ProjectService.rename_sd_project(project, name)

        return project_id

    @staticmethod
    def hard_delete_by_id(project_id: int):
        db_project = Project.query.filter(Project.id == project_id).first()
        if not db_project:
            raise ProjectNotFoundException
        if db_project.sd_root_folder_id:
            DriveUtils.delete_file(db_project.sd_root_folder_id)
        db.session.delete(db_project)
        db.session.commit()

    @staticmethod
    def anonymize_by_id(project_id: int, delete_documents: bool = False) -> Project:
        project = ProjectService.get_by_id(project_id)
        ProjectService.anonymize_project(project, delete_documents=delete_documents)
        return project

    @staticmethod
    def delete_list(projects_id: List[int]):
        """Delete multiple projects"""
        for id in projects_id:
            ProjectService.delete_by_id(id)
        return projects_id

    @staticmethod
    def anonymize_list(projects_id: List[int], delete_documents: bool = False):
        """Anonymize multiple projects """
        for id in projects_id:
            ProjectService.anonymize_by_id(id, delete_documents=delete_documents)
        return projects_id

    @staticmethod
    def anonymize_project(project: Project, delete_documents=False):
        """Anonymize project with corresponding fields maps"""
        anonymization_utils.AnonymizationUtils.anonymize_entity(
            project, PROJECT_ANONYMIZATION_MAP
        )
        anonymization_utils.AnonymizationUtils.anonymize_entity(
            project.requester, REQUESTER_ANONYMIZATION_MAP
        )
        for contact in project.requester.contacts:
            anonymization_utils.AnonymizationUtils.anonymize_entity(
                contact, CONTACT_ANONYMIZATION_MAP
            )
            for phone in contact.phones:
                db.session.delete(phone)
                # anonymization_utils.AnonymizationUtils.anonymize_entity(
                #    phone, PHONE_NUMBER_ANONYMIZATION_MAP
                # )
        for phone in project.requester.phones:
            db.session.delete(phone)
            # anonymization_utils.AnonymizationUtils.anonymize_entity(
            #    phone, PHONE_NUMBER_ANONYMIZATION_MAP
            # )
        for accommodation in project.accommodations:
            anonymization_utils.AnonymizationUtils.anonymize_entity(
                accommodation, ACCOMMODATION_ANONYMIZATION_MAP
            )
            for phone in accommodation.phones:
                db.session.delete(phone)
                # anonymization_utils.AnonymizationUtils.anonymize_entity(
                #    phone, PHONE_NUMBER_ANONYMIZATION_MAP
                # )
        project.anonymized = True
        db.session.commit()

        if delete_documents:
            create_task(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("QUEUES_LOCATION"),
                queue=PROJECT_DELETE_DOCS_QUEUE_NAME,
                uri=f"{request.host_url}_internal/projects/delete-files",
                method="POST",
                payload={"project_id": project.id},
            )

        return "success"

    @staticmethod
    def update_dates_status(new_status, project):
        for status in ProjectDateStatus:
            if new_status == status.value:
                today = date.today()
                setattr(project, status.name, today)
                api.logger.info(f"New status date saved. {status.name} : {today}")
                return
        return

    @staticmethod
    def create_drive_structure(project: Project) -> Project:
        """ Creates the drive structure for a project
        Root
        |-> Devis et Factures
        |-> Logement
          |-> Compte-Rendus
          |-> Photos
        |-> Financeurs
        |-> Demandeur
        """
        client = DriveService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()

        if not project.sd_root_folder_id:
            names = []
            if project.requester.last_name:
                names.append(project.requester.last_name)
            if project.requester.first_name:
                names.append(project.requester.first_name)

            folder_id = DriveUtils.create_folder(
                f"{' '.join(names)} - {project.id}",
                project.mission.sd_projects_folder_id,
            )
            if not folder_id:
                raise SharedDriveException(KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION)
            project.sd_root_folder_id = folder_id

        def batch_folder_callback(request_id, response, exception):
            if exception is not None:
                raise SharedDriveException(KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION)
            else:
                setattr(project, request_id, response.get("id"))

        batch = client.new_batch_http_request(callback=batch_folder_callback)

        for existing, name in [
            ("sd_quotes_folder_id", SD_PROJECT_QUOTES_FOLDER_NAME),
            ("sd_accommodation_folder_id", SD_PROJECT_ACCOMMODATION_FOLDER_NAME),
            ("sd_funders_folder_id", SD_PROJECT_FUNDERS_FOLDER_NAME),
            ("sd_requester_folder_id", SD_PROJECT_REQUESTER_FOLDER_NAME),
        ]:
            if not getattr(project, existing):
                batch.add(
                    DriveUtils.create_folder(
                        name, project.sd_root_folder_id, client=client, batch=True
                    ),
                    request_id=existing,
                )

        if len(batch._order) > 0:
            batch.execute()

        if project.sd_accommodation_folder_id:
            batch = client.new_batch_http_request(callback=batch_folder_callback)
            for existing, name in [
                (
                    "sd_accommodation_report_folder_id",
                    SD_PROJECT_ACCOMMODATION_REPORT_FOLDER_NAME,
                ),
                (
                    "sd_accommodation_pictures_folder_id",
                    SD_PROJECT_ACCOMMODATION_PICTURES_FOLDER_NAME,
                ),
            ]:
                if not getattr(project, existing):
                    batch.add(
                        DriveUtils.create_folder(
                            name,
                            project.sd_accommodation_folder_id,
                            client=client,
                            batch=True,
                        ),
                        request_id=existing,
                    )
            if len(batch._order) > 0:
                batch.execute()

        db.session.commit()

        return project

    @staticmethod
    def add_document(
        project: Project, files_id: List, kind: str, data: dict, user_email: str
    ):
        dest_folder = None
        properties = {
            "projectId": project.id,
            "missionId": project.mission_id,
            "kind": kind,
        }
        if kind == "QUOTE" or kind == "INVOICE":
            dest_folder = project.sd_quotes_folder_id
            if data.get("entity_id", None) is not None:
                properties["entityId"] = data.get("entity_id")
        elif kind == "ACCOMMODATION_REPORT":
            dest_folder = project.sd_accommodation_report_folder_id
        elif kind == "ACCOMMODATION_PICTURE":
            dest_folder = project.sd_accommodation_pictures_folder_id
        elif kind == "FUNDER":
            dest_folder = project.sd_funders_folder_id
        elif kind == "REQUESTER":
            dest_folder = project.sd_requester_folder_id
        elif kind == "ATTACHMENT":
            dest_folder = project.sd_root_folder_id

        response = []

        for file_id in files_id:
            if dest_folder is not None:
                resp = DriveUtils.copy_file(
                    file_id,
                    dest_folder,
                    properties=properties,
                    user_email=user_email,
                    fields=DRIVE_DEFAULT_FIELDS,
                )
                if not resp:
                    raise SharedDriveException(KEY_SHARED_DRIVE_COPY_EXCEPTION)
                else:
                    response.append(resp)

        return response

    @staticmethod
    def rename_sd_project(project: Project, name: str):
        if project.sd_root_folder_id:
            res = DriveUtils.update_file(project.sd_root_folder_id, dict(name=name))
            if not res:
                raise SharedDriveException(KEY_SHARED_DRIVE_RENAME_EXCEPTION)

    @staticmethod
    def get_projects(
        project_ids: List[int], raise_error: bool = False
    ) -> List[Project]:
        projects_dict = {}
        db_projects = Project.query.filter(Project.id.in_(project_ids)).all()
        for db_project in db_projects:
            projects_dict[db_project.id] = db_project
        if raise_error:
            does_not_exist = any(
                project_id not in projects_dict.keys() for project_id in project_ids
            )
            if does_not_exist:
                raise ProjectNotFoundException

        return db_projects

    @staticmethod
    def get_project_locations(term):
        search_term = f"%{term}%"
        db_locations = (
            Project.query.filter(Project.address_location.ilike(search_term))
            .distinct(Project.address_location)
            .all()
        )
        return [
            {"address_location": d.address_location, "id": d.id} for d in db_locations
        ]

    @staticmethod
    def get_project_fields(term: str):
        one_project = Project.query.first()
        one_project_dict = one_project.__dict__
        all_keys = []
        translations = ProjectService.get_project_translations()
        project_keys = list(one_project_dict.keys())
        project_keys.extend(
            [
                'requester.address_location',
                'requester.address_street',
                'project.accommodation.accommodation_type',
                'project.accommodation.condominium',
                'mission.client.name',
                'mission.agency.name',
                'mission.antenna.name',
            ]
        )
        for key in project_keys:
            if key in FORBIDDEN_FIELDS:
                continue
            if "_id" in key or "date" in key:
                continue
            if key not in translations and '.' in key:
                splitted_key = key.split('.')
                if splitted_key[0] not in translations:
                    continue
                if not term or term.lower() in translations[splitted_key[0]][splitted_key[1]].lower():
                    all_keys.append({"key": key, "custom": False})
                    continue
                continue
            if not term or term.lower() in translations[key].lower():
                all_keys.append({"key": key, "custom": False})
        custom_fields = ProjectCustomField.query.distinct(
            ProjectCustomField.custom_field_id
        ).all()
        for c in custom_fields:
            append_field = True
            if not term or term.lower() in c.custom_field.name.lower():
                for k in all_keys:
                    if k.get('label') == c.custom_field.name:
                        append_field = False
                if append_field:
                    all_keys.append(
                        {
                            "label": c.custom_field.name,
                            "custom": True,
                            "key": c.custom_field_id,
                        }
                    )
        return all_keys

    @staticmethod
    def get_project_translations():
        res = requests.get(os.getenv("TRANSLATION_URL"))
        return res.json()["project"]
