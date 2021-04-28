from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_restx import inputs
from flask_sqlalchemy import Pagination

from . import api, CustomField
from .interface import CustomFieldInterface
from .schema import CustomFieldPaginatedSchema, CustomFieldSchema
from .service import (
    CustomFieldService,
    CUSTOM_FIELDS_DEFAULT_PAGE,
    CUSTOM_FIELDS_DEFAULT_PAGE_SIZE,
    CUSTOM_FIELDS_DEFAULT_SORT_FIELD,
    CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class CustomFieldResource(AuthenticatedApi):
    """ CustomFields """

    @accepts(
        *SEARCH_PARAMS,
        dict(name="mission_id", type=int),
        dict(name="fetch_deleted", type=inputs.boolean),
        dict(name="category", type=str),
        api=api,
    )
    @responds(schema=CustomFieldPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all custom_fields """
        return CustomFieldService.get_all(
            page=int(request.args.get("page", CUSTOM_FIELDS_DEFAULT_PAGE)),
            size=int(request.args.get("size", CUSTOM_FIELDS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", CUSTOM_FIELDS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION
            ),
            mission_id=int(request.args.get("mission_id"))
            if request.args.get("mission_id") not in [None, ""]
            else None,
            fetch_deleted=True
            if request.args.get("fetch_deleted") == "True"
            else False,
            category=str(request.args.get("category"))
            if request.args.get("category") not in [None, ""]
            else None,
        )

    @accepts(schema=CustomFieldSchema, api=api)
    @responds(schema=CustomFieldSchema)
    def post(self) -> CustomField:
        """ Create an custom_field """
        return CustomFieldService.create(request.parsed_obj)


@api.route("/<int:custom_field_id>")
@api.param("custom_fieldId", "CustomField unique ID")
class CustomFieldIdResource(AuthenticatedApi):
    @responds(schema=CustomFieldSchema)
    def get(self, custom_field_id: int) -> CustomField:
        """ Get single custom_field """

        return CustomFieldService.get_by_id(custom_field_id)

    def delete(self, custom_field_id: int) -> Response:
        """Delete single custom_field"""

        id = CustomFieldService.delete_by_id(custom_field_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=CustomFieldSchema, api=api)
    @responds(schema=CustomFieldSchema)
    def put(self, custom_field_id: int) -> CustomField:
        """Update single custom_field"""

        changes: CustomFieldInterface = request.parsed_obj
        db_custom_field = CustomFieldService.get_by_id(custom_field_id)
        return CustomFieldService.update(db_custom_field, changes)
