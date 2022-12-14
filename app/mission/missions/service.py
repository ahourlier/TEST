import logging
import os

from flask_sqlalchemy import Pagination
from sqlalchemy import or_

import app.admin.agencies.service as agency_service
import app.admin.antennas.service as antenna_service
import app.admin.clients.service as client_service
from flask import request, g, jsonify
from app import db
from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.antennas.exceptions import AntennaNotFoundException
from app.admin.clients.exceptions import ClientNotFoundException
from app.admin.clients.referents.schema import ReferentSchema
from app.admin.clients.schema import ClientSchema
from app.auth.users.model import UserGroup
from app.common.app_name import App
from app.common.config_error_messages import (
    KEY_SHARED_DRIVE_CREATION_EXCEPTION,
    KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION,
    KEY_GOOGLE_GROUP_CREATION_EXCEPTION,
    KEY_SHARED_DRIVE_PERMISSION_EXCEPTION,
    KEY_SHARED_DRIVE_RENAME_EXCEPTION,
    KEY_SHARED_DRIVE_COPY_EXCEPTION,
    KEY_GOOGLE_GROUP_VISIBILITY_CHANGE_EXCEPTION,
)
from app.common.drive_utils import DriveUtils, DRIVE_DEFAULT_FIELDS
from app.common.exceptions import (
    InconsistentUpdateIdException,
    SharedDriveException,
    GoogleGroupsException,
)
from app.common.google_apis import DriveService, DirectoryService, GroupsSettingsService
from app.common.group_utils import GroupUtils
from app.common.tasks import create_task
from app.common.search import sort_query
from app.mission.missions import Mission, MissionSchema
from app.mission.missions.error_handlers import MissionNotFoundException
from app.mission.missions.exceptions import (
    UnknownMissionTypeException,
    WrongSharedDriveSelectionException,
)
from app.mission.missions.interface import MissionInterface

from app.admin.clients.referents.service import ReferentService
from app.mission.missions.mission_details.exceptions import (
    MissionDetailNotFoundException,
)
from app.mission.missions.mission_details.financial_device.exceptions import (
    FinancialDeviceNotFoundException,
)
from app.mission.missions.mission_details.financial_device.schema import (
    FinancialDeviceSchema,
)
from app.mission.missions.mission_details.financial_device.service import (
    FinancialDeviceService,
)
from app.mission.missions.mission_details.model import MissionDetail
from app.mission.missions.mission_details.schema import MissionDetailSchema
from app.mission.missions.schema import MissionLightSchema

from app.mission.teams import Team

from app.admin.antennas import Antenna
from app.admin.agencies import Agency
from app.admin.clients import Client
from app.auth.users.model import User

import app.auth.users.service as users_service

MISSIONS_DEFAULT_PAGE = 1
MISSIONS_DEFAULT_PAGE_SIZE = 20
MISSIONS_DEFAULT_SORT_FIELD = "created_at"
MISSIONS_DEFAULT_SORT_DIRECTION = "desc"

SD_MISSION_DOC_TEMPLATES_FOLDER_NAME = "Mod??le de documents"
SD_MISSION_DOC_INFO_FOLDER_NAME = "Documents d'information"
SD_MISSION_PROJECTS_FOLDER_NAME = "Projets"

MISSION_INIT_QUEUE_NAME = "mission-queue"

MISSION_DELETE_SD_PREFIX = "ZZ - [ARCHIVE]"

MODEL_MAPPING = {"agency": Agency, "antenna": Antenna, "client": Client, "user": User}


class MissionService:
    @staticmethod
    def get_all(
        page=MISSIONS_DEFAULT_PAGE,
        size=MISSIONS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=MISSIONS_DEFAULT_SORT_FIELD,
        direction=MISSIONS_DEFAULT_SORT_DIRECTION,
        agency_id=None,
        antenna_id=None,
        client_id=None,
        user=None,
        mission_type=None,
    ) -> Pagination:
        import app.mission.permissions as mission_permissions
        from app.mission.teams.service import TeamService

        q = Mission.query

        if "." in sort_by:
            q = MissionService.sort_from_sub_model(q, sort_by, direction)
        elif sort_by == "mission_managers":
            q = MissionService.sort_from_sub_model(q, "user.first_name", direction)
        else:
            q = sort_query(q, sort_by, direction)

        q = q.filter(or_(Mission.is_deleted == False, Mission.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Mission.name.ilike(search_term),
                    Mission.status.ilike(search_term),
                    Mission.comment.ilike(search_term),
                )
            )

        if agency_id is not None:
            q = q.filter(Mission.agency_id == agency_id)
        if antenna_id is not None:
            q = q.filter(Mission.antenna_id == antenna_id)
        if client_id is not None:
            q = q.filter(Mission.client_id == client_id)
        if mission_type is not None:
            if mission_type not in [App.INDIVIDUAL, App.COPRO]:
                raise UnknownMissionTypeException
            else:
                q = q.filter(Mission.mission_type == mission_type)

        q = q.filter(Mission.mission_type == g.user.preferred_app.preferred_app)

        if user is not None:
            q = mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
                q, user
            )

        pagination = q.paginate(page=page, per_page=size)

        for item in pagination.items:
            mission_managers = TeamService.get_all_mission_managers(mission_id=item.id)
            item.managers = mission_managers.items

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(mission_id: int) -> Mission:
        db_mission = Mission.query.get(mission_id)
        if db_mission is None:
            raise MissionNotFoundException
        return db_mission

    @staticmethod
    def create(new_attrs: MissionInterface) -> Mission:
        """Create a new mission with linked agency, antenna, and client"""
        try:
            agency_service.AgencyService.get_by_id(new_attrs.get("agency_id"))
        except AgencyNotFoundException as e:
            raise e
        if new_attrs.get("antenna_id"):
            try:
                antenna_service.AntennaService.get_by_id(new_attrs.get("antenna_id"))
            except AntennaNotFoundException as e:
                raise e
        try:
            client_service.ClientService.get_by_id(new_attrs.get("client_id"))
        except ClientNotFoundException as e:
            raise e
        else:
            referents = None
            if new_attrs.get("referents"):
                referents = new_attrs.get("referents")
                del new_attrs["referents"]

            mission = None

            if new_attrs["mission_type"] == App.COPRO:
                operational_drive_id = new_attrs["sdv2_operationel_drive"]
                administrative_drive_id = new_attrs["sdv2_administratif_drive"]

                administrative_folders = DriveUtils.list_folders(
                    administrative_drive_id, g.user.email, None
                )
                # Check Administratif drive structure
                shared_drive_name = DriveUtils.get_shared_drive_name(
                    administrative_drive_id, g.user.email, None
                )
                for item in administrative_folders:
                    if item["name"] == shared_drive_name:
                        sdv2_administratif_folder_id = item["id"]
                if not sdv2_administratif_folder_id:
                    raise WrongSharedDriveSelectionException()

                (
                    structure,
                    shared_drive_name,
                ) = MissionService.create_operational_drive_structure(
                    operational_drive_id
                )

                mission = Mission(**new_attrs, creator=g.user.email)

                MissionService.link_drive_ids(
                    mission,
                    operational_drive_id,
                    administrative_drive_id,
                    sdv2_administratif_folder_id,
                    structure,
                    shared_drive_name,
                    None,
                )

                db.session.add(mission)
                db.session.commit()
                MissionService.associate_google_group(mission)

                mission_details = MissionDetail()
                mission_details.mission_id = mission.id
                db.session.add(mission_details)
                db.session.commit()

            else:
                mission = Mission(**new_attrs, creator=g.user.email)
                db.session.add(mission)
                db.session.commit()

            if referents:
                for r in referents:
                    r["mission_id"] = mission.id
                    ReferentService.create(r)

            if mission.mission_type == App.INDIVIDUAL:
                create_task(
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("QUEUES_LOCATION"),
                    queue=MISSION_INIT_QUEUE_NAME,
                    uri=f"{os.getenv('API_URL')}/_internal/missions/init-drive",
                    method="POST",
                    payload={
                        "mission_id": mission.id,
                    },
                )
            return mission

    @staticmethod
    def update(
        mission: Mission, changes: MissionInterface, force_update: bool = False
    ) -> Mission:
        # if we find referents, remove them (supposed to used the referent WS)
        if changes.get("referents"):
            del changes["referents"]
        if force_update or MissionService.has_changed(mission, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != mission.id:
                raise InconsistentUpdateIdException()

            if changes.get("mission_type") == App.COPRO:
                operational_drive_id = changes.get("sdv2_operationel_drive")
                administrative_drive_id = changes.get("sdv2_administratif_drive")
                if operational_drive_id and administrative_drive_id:

                    # Check Administratif drive structure
                    administrative_folders = DriveUtils.list_folders(
                        administrative_drive_id, g.user.email, None
                    )

                    shared_drive_name = DriveUtils.get_shared_drive_name(
                        administrative_drive_id, g.user.email, None
                    )
                    for item in administrative_folders:
                        if item["name"] == shared_drive_name:
                            sdv2_administratif_folder_id = item["id"]
                    if not sdv2_administratif_folder_id:
                        raise WrongSharedDriveSelectionException()

                    # Check Operational drive structure

                    (
                        structure,
                        shared_drive_name,
                    ) = MissionService.create_operational_drive_structure(
                        operational_drive_id
                    )

                    MissionService.link_drive_ids(
                        mission,
                        operational_drive_id,
                        administrative_drive_id,
                        sdv2_administratif_folder_id,
                        structure,
                        shared_drive_name,
                        changes,
                    )

                    MissionService.associate_google_group(mission, changes)
            mission.update(changes)
            db.session.commit()
        return mission

    @staticmethod
    def has_changed(mission: Mission, changes: MissionInterface) -> bool:
        for key, value in changes.items():
            if getattr(mission, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(mission_id: int) -> int:
        mission = Mission.query.filter(Mission.id == mission_id).first()
        if not mission:
            raise MissionNotFoundException

        if mission.mission_type == App.INDIVIDUAL:
            import app.project.projects.service as projects_service

            projects_id = [project.id for project in mission.projects]
            projects_service.ProjectService.delete_list(projects_id)

        if mission.mission_type == App.COPRO:
            from app.task.service import TaskService
            from app.common.db_utils import DBUtils

            # Delete all related Tasks and Entity
            TaskService.delete_from_entity_id(mission_id, "mission_id")
            DBUtils.delete_entity_from_mission_id(mission_id)

        mission.soft_delete()
        db.session.commit()
        MissionService.rename_sd(
            mission,
            f"{MISSION_DELETE_SD_PREFIX} {os.getenv('SD_ENV_PREFIX', '')}{mission.name}",
        )
        return mission_id

    @staticmethod
    def create_drive_structure(mission: Mission) -> Mission:
        """Creates the drive structure for a mission
        Root
        |-> Mod??le de documents
        |-> Documents d'information
        |-> Projets
        """

        client = DriveService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()

        if not mission.sd_root_folder_id:
            sd_id = DriveUtils.create_shared_drive(
                f"{os.getenv('SD_ENV_PREFIX', '')}Mission : {mission.name}"
            )
            if not sd_id:
                raise SharedDriveException(KEY_SHARED_DRIVE_CREATION_EXCEPTION)
            mission.sd_root_folder_id = sd_id

        def batch_folder_callback(request_id, response, exception):
            if exception is not None:
                raise SharedDriveException(KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION)
            else:
                setattr(mission, request_id, response.get("id"))

        batch = client.new_batch_http_request(callback=batch_folder_callback)

        for existing, name in [
            ("sd_document_templates_folder_id", SD_MISSION_DOC_TEMPLATES_FOLDER_NAME),
            ("sd_information_documents_folder_id", SD_MISSION_DOC_INFO_FOLDER_NAME),
            ("sd_projects_folder_id", SD_MISSION_PROJECTS_FOLDER_NAME),
        ]:
            if not getattr(mission, existing):
                batch.add(
                    DriveUtils.create_folder(
                        name, mission.sd_root_folder_id, client=client, batch=True
                    ),
                    request_id=existing,
                )

        if len(batch._order) > 0:
            batch.execute()

        db.session.commit()

        return mission

    @staticmethod
    def init_mission_group(mission: Mission):
        """
        Init mission google group
        """

        client = DirectoryService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()

        if not mission.google_group_id:
            group_email = f"{os.getenv('GROUP_EMAIL_ENV_PREFIX', '')}oslo-mission-{mission.code_name}@{os.getenv('GSUITE_DOMAIN')}"
            group_id = GroupUtils.get_google_group(group_email, client=client)
            if not group_id:
                group_id = GroupUtils.create_google_group(
                    email=group_email,
                    name=f"{os.getenv('GROUP_NAME_ENV_PREFIX')}OSLO - Mission {mission.name}",
                    client=client,
                )
            if group_id:
                mission.google_group_id = group_id
                db.session.commit()
            else:
                raise GoogleGroupsException(KEY_GOOGLE_GROUP_CREATION_EXCEPTION)

            groups_client = GroupsSettingsService(
                os.getenv("TECHNICAL_ACCOUNT_EMAIL")
            ).get()
            group_updated = GroupUtils.set_group_visibility_private(
                group_email, client=groups_client
            )
            if not group_updated:
                raise GoogleGroupsException(
                    KEY_GOOGLE_GROUP_VISIBILITY_CHANGE_EXCEPTION
                )

    @staticmethod
    def rename_sd(mission: Mission, name: str):
        if mission.sd_root_folder_id:
            res = DriveUtils.rename_shared_drive(mission.sd_root_folder_id, name)
            if not res:
                raise SharedDriveException(KEY_SHARED_DRIVE_RENAME_EXCEPTION)

    @staticmethod
    def add_document(mission: Mission, files_id: str, kind: str, user_email: str):
        dest_folder = None
        if kind == "ATTACHMENT":
            dest_folder = mission.sd_information_documents_folder_id

        response = []
        for file_id in files_id:
            if dest_folder is not None:
                resp = DriveUtils.copy_file(
                    file_id,
                    dest_folder,
                    properties=dict(missionId=mission.id, kind=kind),
                    user_email=user_email,
                    fields=DRIVE_DEFAULT_FIELDS,
                )
                if not resp:
                    raise SharedDriveException(KEY_SHARED_DRIVE_COPY_EXCEPTION)
                else:
                    response.append(resp)

        return response

    @staticmethod
    def get_details_by_mission_id(mission_id):
        mission_detail = MissionDetail.query.filter(
            MissionDetail.mission_id == mission_id
        ).first()

        if not mission_detail:
            raise MissionDetailNotFoundException

        mission_detail_dump = MissionDetailSchema().dump(mission_detail)

        mission = MissionService.get_by_id(mission_id)

        if not mission:
            raise MissionNotFoundException

        dumped_mission = MissionLightSchema().dump(mission)

        mission_detail_dump["referents"] = (
            [ReferentSchema().dump(r) for r in mission.referents]
            if mission.referents
            else None
        )
        mission_detail_dump["name"] = mission.name
        mission_detail_dump["client"] = (
            ClientSchema().dump(mission.client) if mission.client else None
        )
        mission_detail_dump["mission_start_date"] = dumped_mission["mission_start_date"]
        mission_detail_dump["mission_end_date"] = dumped_mission["mission_end_date"]

        mission_detail_dump["financial_devices"] = []
        try:
            financial_devices = FinancialDeviceService.get_by_mission_detail_id(
                mission_detail.id
            )
            for device in financial_devices:
                obj = FinancialDeviceSchema().dump(device)
                mission_detail_dump["financial_devices"].append(obj)
        except FinancialDeviceNotFoundException:
            pass

        return jsonify(mission_detail_dump)

    def sort_from_sub_model(query, sort_by, direction):
        values = sort_by.split(".")
        sub_model = MODEL_MAPPING[values[len(values) - 2]]
        if sub_model == User:
            query = query.join(Team, isouter=True)
        sort_by = values[len(values) - 1]
        query = query.join(sub_model, isouter=True)
        return sort_query(query, sort_by, direction, sub_model)

    def create_operational_drive_structure(sdv2_operationel_drive_id):
        operational_folders = DriveUtils.list_folders(
            sdv2_operationel_drive_id, g.user.email, None
        )

        MissionService.check_operational_structure_exists(operational_folders)

        shared_drive_name = DriveUtils.get_shared_drive_name(
            sdv2_operationel_drive_id, g.user.email, None
        )

        # Check if root folder with same name as shared drive exists
        found = False
        for file in operational_folders:
            if file["name"] == shared_drive_name:
                found = True
                operational_folder_id = file["id"]
                break

        # If not, bad shared drive selection
        if not found:
            raise WrongSharedDriveSelectionException()

        folders = {
            "10 Suivi animation": None,
            "20 Outils animation": None,
            "30 Equipe et Local": None,
            "40 BDD": None,
            "_10 Imports": None,
            "_20 Exports": None,
        }
        for folder_name in folders.keys():
            if folder_name == "_10 Imports" or folder_name == "_20 Exports":
                folders[folder_name] = DriveUtils.create_folder(
                    folder_name, folders["40 BDD"], g.user.email, None, False
                )
            else:
                folders[folder_name] = DriveUtils.create_folder(
                    folder_name, operational_folder_id, g.user.email, None, False
                )

        folders[shared_drive_name] = operational_folder_id
        return folders, shared_drive_name

    def check_operational_structure_exists(operational_folders):
        matches = [
            "10 Suivi animation",
            "20 Outils animation",
            "30 Equipe et Local",
            "40 BDD",
        ]
        folders = [folder["name"] for folder in operational_folders]

        if all(match in folders for match in matches):
            raise WrongSharedDriveSelectionException()

    def link_drive_ids(
        mission,
        sdv2_operationel_drive_id,
        sdv2_administratif_drive_id,
        sdv2_administratif_folder_id,
        structure,
        shared_drive_name,
        mission_changes=None,
    ):
        if not mission_changes:
            mission.sdv2_operationel_drive = sdv2_operationel_drive_id
            mission.sdv2_administratif_drive = sdv2_administratif_drive_id
            mission.sdv2_operationel_folder = structure[shared_drive_name]
            mission.sdv2_administratif_folder = sdv2_administratif_folder_id
            mission.sdv2_suivi_animation_folder = structure["10 Suivi animation"]
            mission.sdv2_outils_animation_folder = structure["20 Outils animation"]
            mission.sdv2_equipes_locales_folder = structure["30 Equipe et Local"]
            mission.sdv2_bdd_folder = structure["40 BDD"]
            mission.sdv2_exports_folder = structure["_10 Imports"]
            mission.sdv2_imports_folder = structure["_20 Exports"]
        else:
            mission_changes["sdv2_operationel_drive"] = sdv2_operationel_drive_id
            mission_changes["sdv2_administratif_drive"] = sdv2_administratif_drive_id
            mission_changes["sdv2_operationel_folder"] = structure[shared_drive_name]
            mission_changes["sdv2_administratif_folder"] = sdv2_administratif_folder_id
            mission_changes["sdv2_suivi_animation_folder"] = structure[
                "10 Suivi animation"
            ]
            mission_changes["sdv2_outils_animation_folder"] = structure[
                "20 Outils animation"
            ]
            mission_changes["sdv2_equipes_locales_folder"] = structure[
                "30 Equipe et Local"
            ]
            mission_changes["sdv2_bdd_folder"] = structure["40 BDD"]
            mission_changes["sdv2_exports_folder"] = structure["_10 Imports"]
            mission_changes["sdv2_imports_folder"] = structure["_20 Exports"]

    def associate_google_group(mission, mission_changes=None):
        client = DirectoryService(os.getenv("TECHNICAL_ACCOUNT_EMAIL")).get()
        group_email = f"{os.getenv('GROUP_EMAIL_ENV_PREFIX', '')}oslov2-mission-{mission.code_name}@{os.getenv('GSUITE_DOMAIN')}"
        group_id = GroupUtils.get_google_group(group_email, client=client)
        if not group_id:
            logging.info(f"Creating google group with email {group_email}")
            group_id = GroupUtils.create_google_group(
                email=group_email,
                name=f"{os.getenv('GROUP_NAME_ENV_PREFIX')}OSLO V2 - Mission {mission.name}",
                client=client,
            )
            # Set permissions on drives for created mission group
            permission = DriveUtils.insert_permission(
                mission.sdv2_operationel_drive,
                "fileOrganizer",
                "group",
                group_email,
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            permission = DriveUtils.insert_permission(
                mission.sdv2_administratif_drive,
                "fileOrganizer",
                "group",
                group_email,
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            # Set permissions on drives for mission creator
            permission = DriveUtils.insert_permission(
                mission.sdv2_operationel_drive,
                "organizer",
                "user",
                mission.creator,
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            permission = DriveUtils.insert_permission(
                mission.sdv2_administratif_drive,
                "organizer",
                "user",
                mission.creator,
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            # Set permissions on drives for admin group
            permission = DriveUtils.insert_permission(
                mission.sdv2_operationel_drive,
                "organizer",
                "group",
                os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP"),
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

            permission = DriveUtils.insert_permission(
                mission.sdv2_administratif_drive,
                "organizer",
                "group",
                os.getenv("APPLICATION_ADMINS_GOOGLE_GROUP"),
                g.user.email,
                None,
            )
            if not permission:
                raise SharedDriveException(KEY_SHARED_DRIVE_PERMISSION_EXCEPTION)

        if group_id:
            if mission_changes:
                mission_changes["google_group_id"] = group_id
            else:
                mission.google_group_id = group_id

        else:
            raise GoogleGroupsException(KEY_GOOGLE_GROUP_CREATION_EXCEPTION)
