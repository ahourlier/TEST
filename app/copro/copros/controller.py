import os

from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from . import api
from .model import Copro
from .schema import (
    CoproPaginatedSchema,
    CoproCreateSchema,
    CoproSchema,
    CoproUpdateSchema,
)
from .service import (
    CoproService,
    COPRO_DEFAULT_PAGE,
    COPRO_DEFAULT_PAGE_SIZE,
    COPRO_DEFAULT_SORT_DIRECTION,
    COPRO_DEFAULT_SORT_FIELD,
)
from ... import db
from ...common.api import AuthenticatedApi
from ...common.permissions import (
    is_manager,
    is_contributor,
    is_admin,
    filter_response_with_clients_access,
    has_mission_permission,
)
from ...common.search import SEARCH_PARAMS
import app.mission.permissions as missions_permissions
from ...common.tasks import create_task


SEARCH_COPRO_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=str),
]


@api.route("")
class CoprosResource(AuthenticatedApi):
    """ Coproprietes """

    @accepts(
        *SEARCH_COPRO_PARAMS, api=api,
    )
    @responds(schema=CoproPaginatedSchema(), api=api)
    @requires(has_mission_permission)
    def get(self) -> Pagination:
        """ Get all missions """
        return CoproService.get_all(
            page=int(request.args.get("page", COPRO_DEFAULT_PAGE)),
            size=int(request.args.get("size", COPRO_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", COPRO_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", COPRO_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
        )

    @accepts(schema=CoproCreateSchema(), api=api)
    @responds(schema=CoproSchema(), api=api)
    def post(self) -> Copro:
        """ Create a mission """
        return CoproService.create(request.parsed_obj)


@api.route("/<int:copro_id>")
@api.param("coproId", "Copro unique ID")
class CoproIdResource(AuthenticatedApi):
    @responds(schema=CoproSchema(), api=api)
    @requires(is_contributor)
    def get(self, copro_id: int):
        return CoproService.get(copro_id)

    @responds(schema=CoproSchema(), api=api)
    @accepts(schema=CoproUpdateSchema(), api=api)
    @requires(is_contributor)
    def put(self, copro_id: int):
        db_copro = CoproService.get(copro_id)
        return CoproService.update(db_copro, request.parsed_obj, copro_id)

    @requires(is_contributor)
    def delete(self, copro_id: int):
        CoproService.delete(copro_id)
        return jsonify(dict(status="Success", id=copro_id))
