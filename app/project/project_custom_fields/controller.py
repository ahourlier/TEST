from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_restx import inputs
from flask_sqlalchemy import Pagination

from . import api
from .interface import ProjectCustomFieldInterface
from .model import ProjectCustomField
from .schema import ProjectCustomFieldSchema, ProjectCustomFieldPaginatedSchema
from .service import (
    ProjectCustomFieldService,
    PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE,
    PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE_SIZE,
    PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_FIELD,
    PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class ProjectCustomFieldResource(AuthenticatedApi):
    """ ProjectCustomFields """

    @accepts(
        *SEARCH_PARAMS,
        dict(name="project_id", type=int),
        dict(name="category", type=str),
        api=api,
    )
    @responds(schema=ProjectCustomFieldPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all project custom_fields """
        return ProjectCustomFieldService.get_all(
            page=int(request.args.get("page", PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE)),
            size=int(request.args.get("size", PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get(
                "sortBy", PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_FIELD
            ),
            direction=request.args.get(
                "sortDirection", PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION
            ),
            project_id=int(request.args.get("project_id"))
            if request.args.get("project_id") not in [None, ""]
            else None,
            category=str(request.args.get("category"))
            if request.args.get("category") not in [None, ""]
            else None,
        )

    @accepts(schema=ProjectCustomFieldSchema, api=api)
    @responds(schema=ProjectCustomFieldSchema)
    def post(self) -> ProjectCustomField:
        """ Create an project_custom_field """
        return ProjectCustomFieldService.create(request.parsed_obj)


@api.route("/list/<int:project_id>")
@api.param("projectId", "Project unique ID")
class ProjectCustomFieldListResource(AuthenticatedApi):
    """ ProjectCustomFields List """

    @accepts(schema=ProjectCustomFieldSchema(many=True), api=api)
    @responds(schema=ProjectCustomFieldSchema(many=True))
    def post(self, project_id: int) -> ProjectCustomField:
        """ Create an project_custom_field """
        return ProjectCustomFieldService.create_update_list(
            project_id, request.parsed_obj
        )

    @accepts(
        dict(name="category", type=str),
        schema=ProjectCustomFieldSchema(many=True),
        api=api,
    )
    @responds(schema=ProjectCustomFieldSchema(many=True))
    def put(self, project_id: int) -> ProjectCustomField:
        """ Update a project_custom_field """
        return ProjectCustomFieldService.create_update_list(
            project_id,
            request.parsed_obj,
            str(request.args.get("category"))
            if request.args.get("category") not in [None, ""]
            else None,
        )


@api.route("/<int:project_custom_field_id>")
@api.param("project_custom_fieldId", "ProjectCustomField unique ID")
class ProjectCustomFieldIdResource(AuthenticatedApi):
    @responds(schema=ProjectCustomFieldSchema)
    def get(self, project_custom_field_id: int) -> ProjectCustomField:
        """ Get single project_custom_field """

        return ProjectCustomFieldService.get_by_id(project_custom_field_id)

    def delete(self, project_custom_field_id: int) -> Response:
        """Delete single project_custom_field"""

        id = ProjectCustomFieldService.delete_by_id(project_custom_field_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=ProjectCustomFieldSchema, api=api)
    @responds(schema=ProjectCustomFieldSchema)
    def put(self, project_custom_field_id: int) -> ProjectCustomField:
        """Update single project_custom_field"""

        changes: ProjectCustomFieldInterface = request.parsed_obj
        db_project_custom_field = ProjectCustomFieldService.get_by_id(
            project_custom_field_id
        )
        return ProjectCustomFieldService.update(db_project_custom_field, changes)
