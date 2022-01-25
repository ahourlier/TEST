from flask import request, Response, jsonify
from flask_accepts import responds, accepts

from . import api, Monitor
from .interface import MonitorInterface
from .schema import MonitorSchema
from .service import MonitorService, MonitorFieldService
from ...common.api import AuthenticatedApi


@api.route("/<int:monitor_id>")
@api.param("monitorId", "Monitor unique ID")
class MonitorIdResource(AuthenticatedApi):
    @responds(schema=MonitorSchema)
    def get(self, monitor_id: int) -> Monitor:
        """Get single monitor"""

        return MonitorService.get_by_id(monitor_id)

    @accepts(schema=MonitorSchema, api=api)
    @responds(schema=MonitorSchema)
    def put(self, monitor_id: int) -> Monitor:
        """Update single monitor"""

        changes: MonitorInterface = request.parsed_obj
        db_monitor = MonitorService.get_by_id(monitor_id)
        return MonitorService.update(db_monitor, changes)


@api.route("/mission/<int:mission_id>")
@api.param("missionId", "Parent mission unique ID")
class MonitorMissionIdResource(AuthenticatedApi):
    @responds(schema=MonitorSchema)
    def get(self, mission_id: int) -> Monitor:
        """Get single monitor"""
        return MonitorService.get_by_mission_id(mission_id)


@api.route("/field/<int:monitor_field_id>")
@api.param("monitorFieldId", "MonitorField unique ID")
class MonitorFieldIdResource(AuthenticatedApi):
    def delete(self, monitor_field_id: int) -> Response:
        """Delete single monitor_field"""

        return MonitorFieldService.delete_by_id(monitor_field_id)
