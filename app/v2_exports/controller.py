from typing import List
from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from app.v2_exports.model import Exports

from app.v2_exports.schema import ExportsSchema, ExportsPaginatedSchema
from app.v2_exports.service import (
    ExportsService,
    EXPORT_DEFAULT_PAGE,
    EXPORT_DEFAULT_PAGE_SIZE,
    EXPORT_DEFAULT_SORT_DIRECTION,
    EXPORT_DEFAULT_SORT_FIELD,
)
from ..common.api import AuthenticatedApi
from ..common.permissions import has_export_permissions, has_mission_permission
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
class ExportsForMissionResource(AuthenticatedApi):
    """Exports by mission id"""

    @responds(schema=ExportsPaginatedSchema())
    @accepts(*SEARCH_PARAMS, api=api)
    @requires(has_mission_permission)
    def get(self, mission_id: int) -> Pagination:
        """Get all exports"""
        return ExportsService.list(
            page=int(request.args.get("page", EXPORT_DEFAULT_PAGE)),
            size=int(request.args.get("size", EXPORT_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", EXPORT_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", EXPORT_DEFAULT_SORT_DIRECTION),
            mission_id=mission_id,
        )

    @responds(schema=ExportsSchema())
    @accepts(schema=ExportsSchema, api=api)
    @requires(has_mission_permission)
    def post(self, mission_id: int) -> Exports:
        """Create export"""
        payload = request.parsed_obj
        payload["mission_id"] = mission_id
        return ExportsService.launch_export(payload)


@api.route("/<int:export_id>/start")
@api.param("ExportId", "Export unique id")
class ExportsByIdResource(AuthenticatedApi):
    """Exports by mission and export id"""

    @responds(schema=ExportsSchema())
    @requires(has_export_permissions)
    def put(self, export_id) -> Exports:
        """Launch export task"""
        current_export = ExportsService.get(export_id)
        return ExportsService.run_export(current_export)


@api.route("/<int:export_id>")
@api.param("ExportId", "Export unique id")
class ExportsByIdResource(AuthenticatedApi):
    """Exports by mission and export id"""

    @responds(schema=ExportsSchema())
    @requires(has_export_permissions)
    def delete(self, export_id) -> Exports:
        """Launch export task"""
        current_export = ExportsService.get(export_id)
        id = ExportsService.delete_export(current_export, export_id)
        return jsonify(dict(status="Success", id=id))
