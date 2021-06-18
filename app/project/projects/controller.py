import os

from flask_allows import requires
from flask_restx import inputs

from . import api
from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Project
from .interface import ProjectInterface
from .schema import (
    ProjectPaginatedSchema,
    ProjectSchema,
    ProjectUpdateSchema,
    ProjectCreationSchema,
    ProjectDeleteMultipleSchema,
    ProjectDocumentSchema,
    ProjectAnonymizeMultipleSchema,
)

from .service import (
    ProjectService,
    PROJECTS_DEFAULT_PAGE,
    PROJECTS_DEFAULT_PAGE_SIZE,
    PROJECTS_DEFAULT_SORT_FIELD,
    PROJECTS_DEFAULT_SORT_DIRECTION,
    PROJECT_INIT_QUEUE_NAME,
)
from ..accommodations.service import AccommodationService
from ... import db

from ...common.api import AuthenticatedApi
from ...common.permissions import (
    has_mission_permission,
    has_project_permission,
    has_multiple_projects_permission,
    filter_response_with_clients_access,
    has_project_employee_or_client_permission,
)
from ...common.search import SEARCH_PARAMS
import app.project.permissions as projects_permissions
from ...common.tasks import create_task


@api.route("/")
class ProjectResource(AuthenticatedApi):
    """ Projects """

    @filter_response_with_clients_access(
        projects_permissions.ProjectPermission.filter_projects_list_fields
    )
    @accepts(
        *SEARCH_PARAMS,
        dict(name="mission_id", type=int),
        dict(name="requester_id", type=int),
        dict(name="requester_type", type=str),
        dict(name="unique_page", type=inputs.boolean),
        dict(name="filter_on_visit_status", type=inputs.boolean),
        dict(name="filter_on_referrer", type=inputs.boolean),
        api=api,
    )
    @responds(schema=ProjectPaginatedSchema(), api=api)
    def get(self) -> Pagination:
        """ Get all projects """
        return ProjectService.get_all(
            page=int(request.args.get("page", PROJECTS_DEFAULT_PAGE)),
            size=int(request.args.get("size", PROJECTS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", PROJECTS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", PROJECTS_DEFAULT_SORT_DIRECTION
            ),
            mission_id=int(request.args.get("mission_id"))
            if request.args.get("mission_id") not in [None, ""]
            else None,
            requester_id=int(request.args.get("requester_id"))
            if request.args.get("requester_id") not in [None, ""]
            else None,
            requester_type=str(request.args.get("requester_type"))
            if request.args.get("requester_type") not in [None, ""]
            else None,
            unique_page=True if request.args.get("unique_page") == "True" else False,
            filter_on_visit_status=True
            if request.args.get("filter_on_visit_status") == "True"
            else False,
            filter_on_referrer=request.args.get("filter_on_referrer") == "true",
            user=g.user,
        )

    @accepts(schema=ProjectCreationSchema(), api=api)
    @responds(schema=ProjectCreationSchema(), api=api)
    @requires(has_mission_permission)
    def post(self) -> Project:
        """ Create a project """
        return ProjectService.create(request.parsed_obj)


@api.route("/<int:project_id>")
@api.param("projectId", "Project unique ID")
class ProjectIdResource(AuthenticatedApi):
    @filter_response_with_clients_access(
        projects_permissions.ProjectPermission.filter_project_fields
    )
    @responds(schema=ProjectSchema(), api=api)
    @requires(has_project_employee_or_client_permission)
    def get(self, project_id: int) -> Project:
        """ Get single project """
        db_project = ProjectService.get_by_id(project_id)
        if (
            db_project.requester
            and db_project.requester.type == "PO"
            and not db_project.accommodation
        ):
            AccommodationService.create({}, db_project.id)

        if db_project.drive_init not in ["IN PROGRESS", "DONE"]:
            if (
                db_project.sd_root_folder_id
                and db_project.sd_quotes_folder_id
                and db_project.sd_accommodation_folder_id
                and db_project.sd_accommodation_report_folder_id
                and db_project.sd_accommodation_pictures_folder_id
                and db_project.sd_funders_folder_id
                and db_project.sd_requester_folder_id
            ):
                db_project.drive_init = "DONE"
                db.session.commit()
            else:
                db_project.drive_init = "IN PROGRESS"
                db.session.commit()
                create_task(
                    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                    location=os.getenv("QUEUES_LOCATION"),
                    queue=PROJECT_INIT_QUEUE_NAME,
                    uri=f"{request.host_url}_internal/projects/init-drive",
                    method="POST",
                    payload={"project_id": db_project.id,},
                )

        return db_project

    @requires(has_project_permission)
    def delete(self, project_id: int) -> Response:
        """Delete single project"""

        id = ProjectService.delete_by_id(project_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=ProjectUpdateSchema(), api=api)
    @responds(schema=ProjectSchema(), api=api)
    @requires(has_project_permission)
    def put(self, project_id: int) -> Project:
        """Update single project"""

        changes: ProjectInterface = request.parsed_obj
        db_project = ProjectService.get_by_id(project_id)
        return ProjectService.update(db_project, changes)


@api.route("/delete-multiple/")
class ProjectDeleteAllResource(AuthenticatedApi):
    """ Projects """

    @accepts(
        schema=ProjectDeleteMultipleSchema(), api=api,
    )
    @requires(has_multiple_projects_permission)
    def put(self) -> Response:
        """Delete multiple project"""
        projects_id = ProjectService.delete_list(request.parsed_obj.get("projects_id"),)
        return jsonify(dict(status="Success", projects_id=projects_id))


@api.route("/anonymize-multiple/")
class ProjectAnonymizeAllResource(AuthenticatedApi):
    """ Projects anonymization """

    @accepts(
        dict(name="delete_documents", type=inputs.boolean),
        schema=ProjectAnonymizeMultipleSchema,
        api=api,
    )
    @requires(has_multiple_projects_permission)
    def put(self) -> Response:
        """Anonymize multiple project"""
        projects_id = ProjectService.anonymize_list(
            request.parsed_obj.get("projects_id"),
            delete_documents=True
            if request.args.get("delete_documents") == "True"
            else False,
        )
        return jsonify(dict(status="Success", projects_id=projects_id))


@api.route("/<int:project_id>/documents")
@api.param("projectId", "Project unique ID")
class ProjectDocumentResource(AuthenticatedApi):
    # DO NOT DELETE FOR DEBUGGING PURPOSES
    # def get(self, project_id):
    #     client = DriveService(g.user.email).get()
    #     return jsonify(
    #         client.files()
    #         .list(
    #             q=f"appProperties has {{ key='projectId' and value='{project_id}'}}",
    #             supportsAllDrives=True,
    #             includeItemsFromAllDrives=True,
    #         )
    #         .execute()
    #     )

    @accepts(schema=ProjectDocumentSchema, api=api)
    @requires(has_project_permission)
    def post(self, project_id: int):
        db_project = ProjectService.get_by_id(project_id)
        data = request.parsed_obj
        response = ProjectService.add_document(
            db_project, data.get("files_id"), data.get("kind"), data, g.user.email
        )
        return jsonify(response)


@api.route("/locations/")
class ProjectLocation(AuthenticatedApi):
    """ Projects locations """

    @accepts(
        *SEARCH_PARAMS,
        api=api,
    )
    # @requires(has_multiple_projects_permission)
    def get(self) -> Response:
        """Search possible project locations"""
        locations = ProjectService.get_project_locations(
            term=request.args.get("term"),
        )
        return jsonify(dict(status="Success", items=locations))


@api.route("/fields/")
class ProjectFields(AuthenticatedApi):
    """ Projects fields """

    @accepts(
        *SEARCH_PARAMS,
        api=api,
    )
    # @requires(has_multiple_projects_permission)
    def get(self) -> Response:
        """Search possible project fields for filter"""
        fields = ProjectService.get_project_fields(
            term=request.args.get("term"),
        )
        return jsonify(dict(status="Success", items=fields))
