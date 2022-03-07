from flask_sqlalchemy import Pagination
from flask_accepts import accepts, responds
from flask_allows import requires
from flask import request, jsonify, Response, g

from app.common.permissions import (
    has_copro_permissions, has_building_list_permissions, has_building_permissions, is_contributor,
)
from .schema import BuildingSchema, BuildingPaginatedSchema, BuildingCreateSchema, BuildingUpdateSchema
from .service import SEARCH_BUILDINGS_PARAMS, BuildingService, BUILDING_DEFAULT_PAGE, BUILDING_DEFAULT_PAGE_SIZE, \
    BUILDING_DEFAULT_SORT_FIELD, BUILDING_DEFAULT_SORT_DIRECTION
from ..common.api import AuthenticatedApi
from . import api, Building
from ..thematique.schema import ThematiqueMissionSchema


@api.route("")
class BuildingsResource(AuthenticatedApi):
    """ Buildings """

    @accepts(
        *SEARCH_BUILDINGS_PARAMS, api=api,
    )
    @responds(schema=BuildingPaginatedSchema(), api=api)
    @requires(has_building_list_permissions)
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
            cs_id=request.args.get("csId")
            if request.args.get("csId") not in [None, ""]
            else None,
            user=g.user
        )

    @accepts(schema=BuildingCreateSchema(), api=api)
    @responds(schema=BuildingSchema(), api=api)
    @requires(has_copro_permissions, is_contributor)
    def post(self) -> Building:
        return BuildingService.create(request.parsed_obj)


@api.route("/<int:building_id>")
@api.param("buildingId", "Building unique id")
class BuildingsResource(AuthenticatedApi):

    @responds(schema=BuildingSchema(), api=api)
    @requires(has_building_permissions)
    def get(self, building_id):
        return BuildingService.get(building_id)

    @responds(schema=BuildingSchema(), api=api)
    @accepts(schema=BuildingUpdateSchema(), api=api)
    @requires(has_building_permissions, is_contributor)
    def put(self, building_id):
        db_building = BuildingService.get(building_id)
        return BuildingService.update(db_building, building_id, request.parsed_obj)

    @requires(has_building_permissions, is_contributor)
    def delete(self, building_id) -> Response:
        deleted_id = BuildingService.delete(building_id)
        return jsonify(dict(status="Success", id=deleted_id))


@api.route("/<int:building_id>/thematiques")
@api.param("buildingId", "Building unique ID")
class BuildingIdThematiqueResource(AuthenticatedApi):

    @responds(schema=ThematiqueMissionSchema(many=True), api=api)
    @requires(has_building_permissions)
    def get(self, building_id: int):
        return BuildingService.get_thematiques(building_id)
