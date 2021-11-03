from app import db
from app.mission.missions.mission_details.exceptions import (
    MissionDetailNotFoundException,
)
from app.mission.missions.mission_details.model import MissionDetail
from app.mission.missions.mission_details.schema import MissionDetailSchema
from flask import jsonify


class MissionDetailService:
    @staticmethod
    def get_by_id(mission_detail_id):
        mission_detail = MissionDetail.query.get(mission_detail_id)

        if not mission_detail:
            raise MissionDetailNotFoundException

        return mission_detail

    @staticmethod
    def update(db_mission, new_attrs):

        if "id" in new_attrs:
            del new_attrs["id"]

        if "mission_id" in new_attrs:
            del new_attrs["mission_id"]

        if "referents" in new_attrs:
            del new_attrs["referents"]

        db_mission.update(new_attrs)
        db.session.commit()
        return db_mission

    @staticmethod
    def get_by_mission_id(mission_id):
        mission_detail = MissionDetail.query.filter(
            MissionDetail.mission_id == mission_id
        ).first()

        if not mission_detail:
            raise MissionDetailNotFoundException

        return mission_detail
