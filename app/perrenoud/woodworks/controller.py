from flask import request
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from .schema import WoodworkSchema
from .service import WoodworkService
from .. import Woodwork


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class WoodworkScenarioIdResource(AuthenticatedApi):
    @accepts(schema=WoodworkSchema, api=api)
    @responds(schema=WoodworkSchema)
    def post(self, scenario_id: int,) -> Woodwork:
        """Create single woodwork"""

        return WoodworkService.create(request.parsed_obj, scenario_id)
