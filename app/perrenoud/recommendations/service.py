from typing import List

from app import db
from app.common.services_utils import ServicesUtils
from app.perrenoud import Scenario, Recommendation
import app.perrenoud.scenarios.service as scenarios_service


class RecommendationService:
    def get_possible_recommendations_entities(scenario_id: str):
        """From a given scenario_id, fetch all heatings, hot_waters and walls that
        can possibly be injected as recommendations elements"""
        db_scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        entities = db_scenario.walls + db_scenario.heatings + db_scenario.hot_waters
        entities_list = []
        for entity in entities:
            name_field = "heating_name" if entity.__tablename__ == "heating" else "name"
            entities_list.append(
                {
                    "name": getattr(entity, name_field),
                    "element_id": entity.id,
                    "table": entity.__tablename__,
                }
            )
        return entities_list

    @staticmethod
    def create(new_attrs, scenario_id=None, commit=True) -> Recommendation:
        """Create a new recommendation"""
        new_attrs = RecommendationService.reformat_payload(new_attrs)
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        recommendation = Recommendation(**new_attrs)
        db.session.add(recommendation)
        if commit:
            db.session.commit()
        return recommendation

    @staticmethod
    def reformat_payload(payload):
        """Reformat recommendation payload from a schema based format to a flat, sql alchemy format"""
        new_attrs = {
            "scenario_id": payload.get("scenario_id"),
            "recommendation": payload.get("recommendation"),
        }
        if payload.get("element").get("table") == "heating":
            new_attrs["heating_id"] = payload.get("element").get("element_id")
        elif payload.get("element").get("table") == "hot_water":
            new_attrs["hot_water_id"] = payload.get("element").get("element_id")
        else:
            new_attrs["wall_id"] = payload.get("element").get("element_id")
        return new_attrs

    @staticmethod
    def recreate_all(scenario_id, recommendations_list: List):
        """Reemplace all recommendations from a given scenario by newly created recommendations"""
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        scenario.recommendations = []
        for new_recommendation in recommendations_list:
            RecommendationService.create(new_recommendation, scenario_id)

    @staticmethod
    def duplicate(
        base_recommendation,
        clone_scenario_parent_id,
        clone_wall_parent_id=None,
        clone_heating_parent_id=None,
        clone_hot_water_parent_id=None,
    ):
        """Duplicate a recommendation, based on provided cloned parents id"""
        fields_to_treat_separately = [
            "scenario_id",
            "heating_id",
            "hot_water_id",
            "wall_id",
        ]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_recommendation,
            extra_fields_to_remove=fields_to_treat_separately.copy(),
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        if clone_heating_parent_id:
            base_fields["element"] = {
                "table": "heating",
                "element_id": clone_heating_parent_id,
            }
        elif clone_wall_parent_id:
            base_fields["element"] = {
                "table": "wall",
                "element_id": clone_wall_parent_id,
            }
        else:
            base_fields["element"] = {
                "table": "hot_water",
                "element_id": clone_hot_water_parent_id,
            }

        clone_recommendation = RecommendationService.create(base_fields, commit=False)
        db.session.flush()
        return clone_recommendation

    @staticmethod
    def duplicate_all_from_scenario(base_scenario, clone_scenario, children_id_maps):
        """Duplicate all recommendations within a base_scenario"""
        for recommendation in base_scenario.recommendations:
            clone_wall_parent_id = None
            clone_heating_parent_id = None
            clone_hot_water_parent_id = None
            if recommendation.wall_id:
                clone_wall_parent_id = children_id_maps["walls"][recommendation.wall_id]
            if recommendation.heating_id:
                clone_heating_parent_id = children_id_maps["heatings"][
                    recommendation.heating_id
                ]
            if recommendation.hot_water_id:
                clone_hot_water_parent_id = children_id_maps["hot_waters"][
                    recommendation.hot_water_id
                ]
            RecommendationService.duplicate(
                recommendation,
                clone_scenario.id,
                clone_wall_parent_id=clone_wall_parent_id,
                clone_heating_parent_id=clone_heating_parent_id,
                clone_hot_water_parent_id=clone_hot_water_parent_id,
            )
