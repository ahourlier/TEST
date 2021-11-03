from app.mission.missions.mission_details.operational_plan.model import OperationalPlan


class OperationalPlanService:
    @staticmethod
    def get_all():
        return OperationalPlan.query.all()
