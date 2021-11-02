from app.mission.missions.mission_details.job.model import Job


class JobService:

    @staticmethod
    def get_all():
        return Job.query.all()
