from flask_accepts import responds

from app.common.api import AuthenticatedApi
from . import api
from app.perrenoud.recommendations.schema import RecommendationEntitySchema
from app.perrenoud.recommendations.service import RecommendationService


@api.route("/scenario_list/<int:scenario_id>")
@api.param("antennaId", "Antenna unique ID")
class RecommendationHelperResource(AuthenticatedApi):
    @responds(schema=RecommendationEntitySchema(many=True))
    def get(self, scenario_id: int):
        """Fetch possible recommendations"""
        return RecommendationService.get_possible_recommendations_entities(scenario_id)
