from flask import request
from flask_accepts import accepts
from flask_allows import requires

from . import data_import_api
from .schema import DataImportSchema
import app.data_import.service as data_import_service
from ..common.api import AuthenticatedApi
from ..common.permissions import is_contributor
import app.mission.missions.service as missions_service


@data_import_api.route("/projects/")
class DocumentResource(AuthenticatedApi):
    @accepts(schema=DataImportSchema, api=data_import_api)
    @requires(is_contributor)
    def post(self):
        """ Import projects data from a sheet and instantiate it into db """
        data = request.parsed_obj
        db_mission = missions_service.MissionService.get_by_id(data.get("mission_id"))
        return data_import_service.DataImportService.import_projects(
            db_mission, data.get("data_sheet_id")
        )
