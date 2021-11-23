from flask_sqlalchemy import Pagination
from flask_accepts import accepts, responds
from flask_allows import requires
from flask import request

from .schema import BuildingSchema, BuildingPaginatedSchema, BuildingCreateSchema
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
