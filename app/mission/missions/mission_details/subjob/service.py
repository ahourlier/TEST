from app.mission.missions.mission_details.subjob.model import Subjob


class SubjobService:
    @staticmethod
    def get_all():
        return Subjob.query.all()
