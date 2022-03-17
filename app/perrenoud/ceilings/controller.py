from flask import request
from flask_accepts import accepts, responds

from app.common.api import AuthenticatedApi

from . import api
from .schema import CeilingSchema
from .service import CeilingService
from .. import Ceiling


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class CeilingScenarioIdResource(AuthenticatedApi):
    @accepts(schema=CeilingSchema, api=api)
    @responds(schema=CeilingSchema)
    def post(self, scenario_id: int,) -> Ceiling:
        """Create single ceiling"""

        return CeilingService.create(request.parsed_obj, scenario_id)
