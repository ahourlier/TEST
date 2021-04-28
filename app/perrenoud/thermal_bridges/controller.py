from flask import request
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from .schema import ThermalBridgeSchema
from .service import ThermalBridgeService
from .. import ThermalBridge


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class ThermalBridgeScenarioIdResource(AuthenticatedApi):
    @accepts(schema=ThermalBridgeSchema, api=api)
    @responds(schema=ThermalBridgeSchema)
    def post(self, scenario_id: int,) -> ThermalBridge:
        """Create single thermal_bridge"""

        return ThermalBridgeService.create(request.parsed_obj, scenario_id)
