from flask_sqlalchemy import Pagination
from flask_accepts import accepts, responds
from flask_allows import requires
from flask import request, jsonify, Response

from .schema import BuildingSchema, BuildingPaginatedSchema, BuildingCreateSchema, BuildingUpdateSchema
from .service import SEARCH_BUILDINGS_PARAMS, BuildingService, BUILDING_DEFAULT_PAGE, BUILDING_DEFAULT_PAGE_SIZE, \
    BUILDING_DEFAULT_SORT_FIELD, BUILDING_DEFAULT_SORT_DIRECTION
from ..common.api import AuthenticatedApi
from . import api, Building


@api.route("")
class BuildingsResource(AuthenticatedApi):
    """ Buildings """

    @accepts(
        *SEARCH_BUILDINGS_PARAMS, api=api,
    )
    @responds(schema=BuildingPaginatedSchema(), api=api)
    # @requires(has_copro_permission)
    def get(self) -> Pagination:
        return BuildingService.list(
            page=int(request.args.get("page", BUILDING_DEFAULT_PAGE)),
            size=int(request.args.get("size", BUILDING_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", BUILDING_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", BUILDING_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
            copro_id=request.args.get("coproId")
            if request.args.get("coproId") not in [None, ""]
            else None,
        )

    @accepts(schema=BuildingCreateSchema(), api=api)
    @responds(schema=BuildingSchema(), api=api)
    def post(self) -> Building:
        return BuildingService.create(request.parsed_obj)


@api.route("/<int:building_id>")
@api.param("buildingId", "Building unique id")
class BuildingsResource(AuthenticatedApi):

    @responds(schema=BuildingSchema(), api=api)
    def get(self, building_id):
        return BuildingService.get(building_id)

    @responds(schema=BuildingSchema(), api=api)
    @accepts(schema=BuildingUpdateSchema(), api=api)
    def put(self, building_id):
        db_building = BuildingService.get(building_id)
        return BuildingService.update(db_building, building_id, request.parsed_obj)

    def delete(self, building_id) -> Response:
        deleted_id = BuildingService.delete(building_id)
        return jsonify(dict(status="Success", id=deleted_id))
