from typing import List
from flask import request

from flask_accepts import responds, accepts

from . import api
from .schema import FunderMonitoringValueByFunderSchema
from .service import FunderMonitoringValueService
from ...common.api import AuthenticatedApi


@api.route("/<int:project_id>")
@api.param("projectId", "Project unique ID")
class ProjectFunderMonitoringValueResource(AuthenticatedApi):
    @responds(schema=FunderMonitoringValueByFunderSchema(many=True))
    def get(self, project_id: int) -> List:
        """Fetch all field by project_id (sorted by funder)"""
        return FunderMonitoringValueService.fetch_project_fields_funders(project_id)

    @accepts(schema=FunderMonitoringValueByFunderSchema(many=True), api=api)
    @responds(schema=FunderMonitoringValueByFunderSchema(many=True))
    def put(self, project_id: int) -> List:
        """Update provided list of project monitored fields"""
        changes = request.parsed_obj
        return FunderMonitoringValueService.update_list(project_id, changes)
