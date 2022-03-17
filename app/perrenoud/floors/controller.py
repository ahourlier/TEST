from flask import request
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from .schema import FloorSchema
from .service import FloorService
from .. import Floor


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class FloorScenarioIdResource(AuthenticatedApi):
    @accepts(schema=FloorSchema, api=api)
    @responds(schema=FloorSchema)
    def post(self, scenario_id: int,) -> Floor:
        """Create single floor"""

        return FloorService.create(request.parsed_obj, scenario_id)
