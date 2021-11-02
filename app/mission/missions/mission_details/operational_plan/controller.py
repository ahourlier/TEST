from app.common.api import AuthenticatedApi
from .. import api
from .service import OperationalPlanService


@api.route("/operational_plan")
class OperationalPlanResource(AuthenticatedApi):

    # @responds(schema=[JobSchema()], api=api)
    def get(self):
        return OperationalPlanService.get_all()

