from app.common.api import AuthenticatedApi
from . import api
from .schema import OperationalPlanSchema
from .service import OperationalPlanService
from flask_accepts import responds


@api.route("")
class OperationalPlanResource(AuthenticatedApi):

    @responds(schema=OperationalPlanSchema, many=True, api=api)
    def get(self):
        return OperationalPlanService.get_all()

