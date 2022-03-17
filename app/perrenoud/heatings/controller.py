from flask import request
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from .schema import HeatingSchema
from .service import HeatingService
from .. import Heating


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class HeatingScenarioIdResource(AuthenticatedApi):
    @accepts(schema=HeatingSchema, api=api)
    @responds(schema=HeatingSchema)
    def post(self, scenario_id: int,) -> Heating:
        """Create single heating"""

        return HeatingService.create(request.parsed_obj, scenario_id)
