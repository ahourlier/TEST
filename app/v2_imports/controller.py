from typing import List
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from app.v2_imports.model import Imports

from app.v2_imports.schema import ImportsSchema, ImportsPaginatedSchema
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


@api.route("/<int:mission_id>")
@api.param("MissionId", "Mission unique id")
class ImportsForMissionResource(AuthenticatedApi):
    """Imports by mission id"""

    @responds(schema=ImportsPaginatedSchema())
    @accepts(*SEARCH_PARAMS, api=api)
    @requires(has_mission_permission)
    def get(self) -> Pagination:
        """Get all imports"""
        pass

    @responds(schema=ImportsSchema())
    @accepts(schema=ImportsSchema, api=api)
    @requires(has_mission_permission)
    def post(self) -> Imports:
        """Create import"""
        pass


@api.route("/<int:mission_id>/<int:import_id>")
@api.param("MissionId", "Mission unique id")
@api.param("ImportId", "Import unique id")
class ImportsByIdResource(AuthenticatedApi):
    """Imports by mission and import id"""

    @responds(schema=ImportsSchema())
    @requires(has_mission_permission)
    def put(self) -> Imports:
        """Launch import task"""
        pass
