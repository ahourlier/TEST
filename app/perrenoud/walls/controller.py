from flask import request
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from .schema import WallSchema
from .service import WallService
from .. import Wall


@api.route("/scenario/<int:scenario_id>")
@api.param("scenarioId", "Scenario unique ID")
class WallScenarioIdResource(AuthenticatedApi):
    @accepts(schema=WallSchema, api=api)
    @responds(schema=WallSchema)
    def post(self, scenario_id: int,) -> Wall:
        """Create single wall"""

        return WallService.create(request.parsed_obj, scenario_id)
