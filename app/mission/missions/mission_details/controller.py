from flask_accepts import accepts, responds
from flask import request
from app.common.api import AuthenticatedApi
from . import api, MissionDetail
from .interface import MissionDetailInterface
from .schema import MissionDetailSchema
from .service import MissionDetailService


@api.route("/<int:mission_detail_id>")
@api.param("missionDetailId", "Mission detail unique ID")
class MissionDetailsResource(AuthenticatedApi):
    """ Mission Details """

    @responds(schema=MissionDetailSchema(), api=api)
    def get(self, mission_detail_id) -> MissionDetail:
        return MissionDetailService.get_by_id(mission_detail_id)

    @responds(schema=MissionDetailSchema(), api=api)
    @accepts(schema=MissionDetailSchema(), api=api)
    def put(self, mission_detail_id):
        changes: MissionDetailInterface = request.parsed_obj
        db_mission_details = MissionDetailService.get_by_id(mission_detail_id)
        return MissionDetailService.update(db_mission_details, changes)
