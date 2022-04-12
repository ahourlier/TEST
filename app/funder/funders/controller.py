from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, FunderSchema, Funder
from .interface import FunderInterface
from .schema import FunderPaginatedSchema, FunderDuplicateSchema
from .service import (
    FunderService,
    FUNDERS_DEFAULT_SORT_DIRECTION,
    FUNDERS_DEFAULT_SORT_FIELD,
    FUNDERS_DEFAULT_PAGE_SIZE,
    FUNDERS_DEFAULT_PAGE,
)
from app.common.api import AuthenticatedApi
from app.common.permissions import can_manage_funders
from app.common.search import SEARCH_PARAMS


@api.route("/")
class FunderResource(AuthenticatedApi):
    """Funders"""

    @accepts(*SEARCH_PARAMS, dict(name="requester_type", type=str), api=api)
    @responds(schema=FunderPaginatedSchema)
    def get(self) -> Pagination:
        """Get all funders"""
        return FunderService.get_all(
            page=int(request.args.get("page", FUNDERS_DEFAULT_PAGE)),
            size=int(request.args.get("size", FUNDERS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", FUNDERS_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", FUNDERS_DEFAULT_SORT_DIRECTION),
            mission_id=int(request.args.get("mission_id"))
            if request.args.get("mission_id")
            else None,
            requester_type=str(request.args.get("requester_type"))
            if request.args.get("requester_type") not in [None, ""]
            else None,
        )

    @accepts(schema=FunderSchema, api=api)
    @responds(schema=FunderSchema, api=api)
    @requires(can_manage_funders)
    def post(self) -> Funder:
        """Create a funder"""

        return FunderService.create(request.parsed_obj, commit=True)


@api.route("/<int:funder_id>")
@api.param("funderId", "Funder unique ID")
class FunderIdResource(AuthenticatedApi):
    @responds(schema=FunderSchema, api=api)
    def get(self, funder_id: int) -> Funder:
        """Get single funder"""
        return FunderService.get_by_id(funder_id)

    @requires(can_manage_funders)
    def delete(self, funder_id: int) -> Response:
        """Delete a funder"""
        id = FunderService.delete_by_id(funder_id, commit=True)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=FunderSchema, api=api)
    @responds(schema=FunderSchema, api=api)
    @requires(can_manage_funders)
    def put(self, funder_id: int) -> Funder:
        """Update a single funder"""

        changes: FunderInterface = request.parsed_obj
        db_funder = FunderService.get_by_id(funder_id)
        return FunderService.update(db_funder, changes, commit=True)


@api.route("/<int:funder_id>/copy-to-mission")
class FunderIdDuplicateResource(AuthenticatedApi):
    @accepts(schema=FunderDuplicateSchema, api=api)
    @responds(schema=FunderSchema, api=api)
    @requires(can_manage_funders)
    def post(self, funder_id: int) -> Funder:
        db_funder = FunderService.get_by_id(funder_id)
        return FunderService.copy_to_mission(
            db_funder, request.parsed_obj["mission_id"], commit=True
        )


@api.route("/copy-to-mission")
class FunderIdDuplicateResource(AuthenticatedApi):
    @accepts(schema=FunderDuplicateSchema, api=api)
    @responds(schema=FunderSchema(many=True), api=api)
    @requires(can_manage_funders)
    def post(self) -> Funder:
        return FunderService.copy_multiple_to_mission(
            mission_id=request.parsed_obj["mission_id"],
            funders_id=request.parsed_obj.get("funders_id"),
        )
