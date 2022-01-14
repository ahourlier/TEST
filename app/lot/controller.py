from flask import request, jsonify, g
from flask_allows import requires
from flask_accepts import accepts, responds

from . import api
from .schema import LotPaginatedSchema, LotCreateSchema, LotSchema, LotUpdateSchema
from .service import (
    LotService,
    LOT_DEFAULT_PAGE,
    LOT_DEFAULT_PAGE_SIZE,
    LOT_DEFAULT_SORT_FIELD,
    LOT_DEFAULT_SORT_DIRECTION,
)
from app.common.permissions import (
    is_contributor,
    has_lot_permissions,
    has_lot_list_permissions,
    has_copro_permissions,
)
from ..common.api import AuthenticatedApi
from ..thematique.schema import ThematiqueMissionSchema

SEARCH_LOTS_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=int),
    dict(name="coproId", type=int),
    dict(name="buildingId", type=int),
]


@api.route("")
class LotsResource(AuthenticatedApi):
    @accepts(
        *SEARCH_LOTS_PARAMS, api=api,
    )
    @responds(schema=LotPaginatedSchema(), api=api)
    @requires(has_lot_list_permissions)
    def get(self):
        return LotService.list(
            page=int(request.args.get("page", LOT_DEFAULT_PAGE)),
            size=int(request.args.get("size", LOT_DEFAULT_PAGE_SIZE)),
            sort_by=request.args.get("sortBy", LOT_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", LOT_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
            copro_id=request.args.get("coproId")
            if request.args.get("coproId") not in [None, ""]
            else None,
            building_id=request.args.get("buildingId")
            if request.args.get("buildingId") not in [None, ""]
            else None,
            user=g.user,
        )

    @accepts(schema=LotCreateSchema(), api=api)
    @responds(schema=LotSchema(), api=api)
    @requires(has_copro_permissions)
    def post(self):
        return LotService.create(request.parsed_obj)


@api.route("/<int:lot_id>")
@api.param("lotId", "Lot unique id")
class LotsIdResource(AuthenticatedApi):
    @responds(schema=LotSchema, api=api)
    @requires(has_lot_permissions)
    def get(self, lot_id):
        return LotService.get(lot_id)

    @responds(schema=LotSchema, api=api)
    @accepts(schema=LotUpdateSchema, api=api)
    @requires(has_lot_permissions)
    def put(self, lot_id):
        db_lot = LotService.get(lot_id)
        return LotService.update(db_lot, request.parsed_obj)

    @requires(has_lot_permissions)
    def delete(self, lot_id):
        id = LotService.delete(lot_id)
        return jsonify(dict(status="Success", id=id))


@api.route("/<int:lot_id>/thematiques")
@api.param("lotId", "Lot unique ID")
class LotIdThematiqueResource(AuthenticatedApi):
    @responds(schema=ThematiqueMissionSchema(many=True), api=api)
    @requires(has_lot_permissions)
    def get(self, lot_id: int):
        return LotService.get_thematiques(lot_id)
