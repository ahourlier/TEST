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
from ...common.api import AuthenticatedApi
from ...common.permissions import (
    is_contributor,
    has_mission_permission,
    has_copro_list_permissions,
    has_copro_permissions,
)
from ...thematique.schema import ThematiqueMissionSchema

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
    @requires(has_copro_list_permissions)
    def get(self) -> Pagination:
        """ Get all coproprietes """
        return CoproService.get_all(
            page=int(request.args.get("page", COPRO_DEFAULT_PAGE)),
            size=int(request.args.get("size", COPRO_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", COPRO_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", COPRO_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
            user=g.user,
        )

    @accepts(schema=CoproCreateSchema(), api=api)
    @responds(schema=CoproSchema(), api=api)
    @requires(has_mission_permission, is_contributor)
    def post(self) -> Copro:
        """ Create a mission """
        return CoproService.create(request.parsed_obj)


@api.route("/<int:copro_id>")
@api.param("coproId", "Copro unique ID")
class CoproIdResource(AuthenticatedApi):
    @responds(schema=CoproSchema(), api=api)
    @requires(has_copro_permissions)
    def get(self, copro_id: int):
        return CoproService.get(copro_id)

    @responds(schema=CoproSchema(), api=api)
    @accepts(schema=CoproUpdateSchema(), api=api)
    @requires(has_copro_permissions, is_contributor)
    def put(self, copro_id: int):
        db_copro = CoproService.get(copro_id)
        return CoproService.update(db_copro, request.parsed_obj, copro_id)

    @requires(has_copro_permissions, is_contributor)
    def delete(self, copro_id: int):
        CoproService.delete(copro_id)
        return jsonify(dict(status="Success", id=copro_id))


@api.route("/<int:copro_id>/thematiques")
@api.param("coproId", "Copro unique ID")
class CoproIdThematiqueResource(AuthenticatedApi):
    @responds(schema=ThematiqueMissionSchema(many=True), api=api)
    @requires(has_copro_permissions, is_contributor)
    def get(self, copro_id: int):
        return CoproService.get_thematiques(copro_id)
