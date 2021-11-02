from app import db
from app.mission.missions.mission_details import MissionDetail
from app.mission.missions.mission_details.exceptions import MissionDetailNotFoundException


class MissionDetailService:

    @staticmethod
    def get_by_id(mission_detail_id):
        mission_detail = MissionDetail.query.get(mission_detail_id)

        if not mission_detail:
            raise MissionDetailNotFoundException

        return mission_detail

    @staticmethod
    def update(db_mission, new_attrs):
        db_mission.update(new_attrs)
        db.session.commit()
        return db_mission
