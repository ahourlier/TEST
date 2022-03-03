from typing import List
from flask import request
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from app.v2_imports.model import Imports

from app.v2_imports.schema import ImportsSchema, ImportsPaginatedSchema
from app.v2_imports.service import (
    ImportsService,
    IMPORT_DEFAULT_PAGE,
    IMPORT_DEFAULT_PAGE_SIZE,
    IMPORT_DEFAULT_SORT_DIRECTION,
    IMPORT_DEFAULT_SORT_FIELD,
)
from ..common.api import AuthenticatedApi
from ..common.permissions import has_mission_permission
from . import api


SEARCH_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
]


@api.route("/mission/<int:mission_id>")
@api.param("MissionId", "Mission unique id")
class ImportsForMissionResource(AuthenticatedApi):
    """Imports by mission id"""

    @responds(schema=ImportsPaginatedSchema())
    @accepts(*SEARCH_PARAMS, api=api)
    @requires(has_mission_permission)
    def get(self, mission_id: int) -> Pagination:
        """Get all imports"""
        return ImportsService.list(
            page=int(request.args.get("page", IMPORT_DEFAULT_PAGE)),
            size=int(request.args.get("size", IMPORT_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", IMPORT_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", IMPORT_DEFAULT_SORT_DIRECTION),
            mission_id=mission_id,
        )

    @responds(schema=ImportsSchema())
    @accepts(schema=ImportsSchema, api=api)
    @requires(has_mission_permission)
    def post(self, mission_id: int) -> Imports:
        """Create import"""
        payload = request.parsed_obj
        payload["mission_id"] = mission_id
        return ImportsService.launch_import(payload)


@api.route("/<int:import_id>/start")
@api.param("ImportId", "Import unique id")
class ImportsByIdResource(AuthenticatedApi):
    """Imports by mission and import id"""

    @responds(schema=ImportsSchema())
    @requires(has_mission_permission)
    def put(self, import_id) -> Imports:
        """Launch import task"""
        current_import = ImportsService.get(import_id)
        return ImportsService.run_import(current_import)
