from enum import Enum

import requests
from flask_sqlalchemy import Pagination
from sqlalchemy import or_
import logging

from app.admin.error_handlers import InconsistentUpdateIdException
from app.common.search import sort_query
from app import db
from app.common.services_utils import ServicesUtils
from app.common.xml_utils import XMLBuilder, PerrenoudParser
from .perrenoud_xml_config import XML_PERRENOUD_CONFIGURATION
from app.perrenoud.scenarios import Scenario
from app.perrenoud.scenarios.error_handlers import (
    ScenarioNotFoundException,
    InitialStateAlreadyCreatedException,
    PerrenoudWebserviceException,
    MissingPerrenoudDataException,
)
from app.perrenoud.scenarios.interface import ScenarioInterface
import app.perrenoud.heatings.service as heatings_service
import app.perrenoud.hot_waters.service as hot_waters_service
import app.perrenoud.walls.service as walls_service
import app.perrenoud.woodworks.service as woodworks_service
import app.perrenoud.ceilings.service as ceilings_service
import app.perrenoud.floors.service as floors_service
import app.perrenoud.thermal_bridges.service as thermal_bridges_service
import app.perrenoud.rooms.service as rooms_service
import app.perrenoud.recommendations.service as recommendations_service
from ...common.app_configuration.service import AppConfigService

SCENARIOS_DEFAULT_PAGE = 1
SCENARIOS_DEFAULT_PAGE_SIZE = 100
SCENARIOS_DEFAULT_SORT_FIELD = "id"
SCENARIOS_DEFAULT_SORT_DIRECTION = "asc"

SCENARIOS_CHILDREN = [
    "heatings",
    "hot_waters",
    "walls",
    "woodworks",
    "ceilings",
    "floors",
    "thermal_bridges",
    "rooms",
    "recommendations_list",
]


class ScenarioSections(Enum):
    EQUIPMENT = "equipments"
    ASSETS_TYPES = "asset_types"
    ROOMS = "rooms"
    RECOMMENDATIONS = "recommendations"


class ScenarioService:
    @staticmethod
    def get_all(
        accommodation_id,
        page=SCENARIOS_DEFAULT_PAGE,
        size=SCENARIOS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=SCENARIOS_DEFAULT_SORT_FIELD,
        direction=SCENARIOS_DEFAULT_SORT_DIRECTION,
        include_initial_state=False,
    ) -> Pagination:
        q = sort_query(Scenario.query, sort_by, direction)
        q = q.filter(Scenario.accommodation_id == accommodation_id)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(or_(Scenario.name.ilike(search_term),))
        if not include_initial_state:
            q = q.filter(Scenario.is_initial_state == False)
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(scenario_id: str) -> Scenario:
        db_scenario = Scenario.query.get(scenario_id)
        if db_scenario is None:
            raise ScenarioNotFoundException
        return db_scenario

    @staticmethod
    def get_initial_state_by_accommodation_id(accommodation_id: str) -> Scenario:
        db_scenario = (
            Scenario.query.filter(Scenario.accommodation_id == accommodation_id)
            .filter(Scenario.is_initial_state == True)
            .first()
        )
        if not db_scenario:
            return ScenarioService.create(
                {"accommodation_id": accommodation_id, "is_initial_state": True}
            )
        return db_scenario

    @staticmethod
    def create(new_attrs: ScenarioInterface, commit=True) -> Scenario:
        """Create a new scenario"""
        if not new_attrs.get("is_initial_state"):
            new_attrs["is_initial_state"] = False
        if new_attrs.get("is_initial_state") is True:
            prior_initial_state = (
                Scenario.query.filter(Scenario.is_initial_state == "True")
                .filter(Scenario.accommodation_id == new_attrs.get("accommodation_id"))
                .first()
            )
            if prior_initial_state:
                raise InitialStateAlreadyCreatedException()
        ServicesUtils.clean_attrs(new_attrs, SCENARIOS_CHILDREN)
        scenario = Scenario(**new_attrs)
        db.session.add(scenario)
        if commit:
            db.session.commit()
        return scenario

    @staticmethod
    def update_energy_gain(initial_state: Scenario, annual_energy_consumption: float):
        scenarios = Scenario.query.filter(
            Scenario.accommodation_id == initial_state.accommodation_id,
            Scenario.is_initial_state == False,
        ).all()
        for scenario in scenarios:
            if (
                annual_energy_consumption
                and scenario.annual_energy_consumption is not None
            ):
                scenario.energy_gain = round(
                    100
                    * (annual_energy_consumption - scenario.annual_energy_consumption)
                    / annual_energy_consumption
                )
            else:
                scenario.energy_gain = None

    @staticmethod
    def update(
        scenario: Scenario,
        changes: ScenarioInterface,
        force_update: bool = True,
        section: str = None,
    ) -> Scenario:
        if force_update or ScenarioService.has_changed(scenario, changes):
            # If one tries to update entity id, a error must be raised
            extracted_fields = ServicesUtils.clean_attrs(
                changes, SCENARIOS_CHILDREN + ["is_initial_state"]
            )
            if changes.get("id") and changes.get("id") != scenario.id:
                raise InconsistentUpdateIdException()
            if (
                scenario.is_initial_state
                and scenario.annual_energy_consumption
                != changes.get("annual_energy_consumption")
            ):
                ScenarioService.update_energy_gain(
                    scenario, changes.get("annual_energy_consumption")
                )
            scenario.update(changes)
            if section == ScenarioSections.EQUIPMENT.value:
                heatings_service.HeatingService.create_update_list(
                    scenario.id, extracted_fields.get("heatings")
                )
                hot_waters_service.HotWaterService.create_update_list(
                    scenario.id, extracted_fields.get("hot_waters")
                )
            if section == ScenarioSections.ASSETS_TYPES.value:
                walls_service.WallService.create_update_list(
                    scenario.id, extracted_fields.get("walls")
                )
                woodworks_service.WoodworkService.create_update_list(
                    scenario.id, extracted_fields.get("woodworks")
                )
                ceilings_service.CeilingService.create_update_list(
                    scenario.id, extracted_fields.get("ceilings")
                )
                floors_service.FloorService.create_update_list(
                    scenario.id, extracted_fields.get("floors")
                )
                thermal_bridges_service.ThermalBridgeService.create_update_list(
                    scenario.id, extracted_fields.get("thermal_bridges")
                )
            if section == ScenarioSections.ROOMS.value:
                rooms_service.RoomService.create_update_list(
                    scenario.id, extracted_fields.get("rooms")
                )
            if (
                section == ScenarioSections.RECOMMENDATIONS.value
                and "recommendations_list" in extracted_fields
            ):
                recommendations_service.RecommendationService.recreate_all(
                    scenario.id, extracted_fields.get("recommendations_list")
                )

            db.session.commit()
        return scenario

    @staticmethod
    def has_changed(scenario: Scenario, changes: ScenarioInterface) -> bool:
        for key, value in changes.items():
            if getattr(scenario, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(scenario_id: int) -> int or None:
        scenario = Scenario.query.filter(Scenario.id == scenario_id).first()
        if not scenario:
            raise ScenarioNotFoundException
        db.session.delete(scenario)
        db.session.commit()
        return scenario_id

    @staticmethod
    def create_and_duplicate(accommodation_id):
        initial_state = ScenarioService.get_initial_state_by_accommodation_id(
            accommodation_id
        )
        return ScenarioService.duplicate(initial_state.id)

    @staticmethod
    def duplicate(scenario_id: int) -> Scenario:
        """Duplicate a scenario, all his children and sub-children"""
        base_scenario = ScenarioService.get_by_id(scenario_id)
        fields_to_treat_separately = ["is_initial_state"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_scenario, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["is_initial_state"] = False
        base_fields["name"] = ScenarioService.get_new_scenario_name(base_scenario)
        clone_scenario = ScenarioService.create(base_fields, commit=True)

        # Duplicate children
        children_id_maps = {}
        children_id_maps[
            "heatings"
        ] = heatings_service.HeatingService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "ceilings"
        ] = ceilings_service.CeilingService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "floors"
        ] = floors_service.FloorService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "hot_waters"
        ] = hot_waters_service.HotWaterService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "thermal_bridges"
        ] = thermal_bridges_service.ThermalBridgeService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "walls"
        ] = walls_service.WallService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        children_id_maps[
            "woodworks"
        ] = woodworks_service.WoodworkService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario
        )
        rooms_service.RoomService.duplicate_all_from_scenarios(
            base_scenario, clone_scenario, children_id_maps
        )
        recommendations_service.RecommendationService.duplicate_all_from_scenario(
            base_scenario, clone_scenario, children_id_maps
        )
        db.session.commit()
        return clone_scenario

    @staticmethod
    def launch_perrenoud_analysis(scenario_id: str, test_XML=False):
        """Launch Perrenoud calculs and return results"""
        db_scenario = Scenario.query.get(scenario_id)
        if db_scenario is None:
            raise ScenarioNotFoundException
        xml_builder = XMLBuilder(XML_PERRENOUD_CONFIGURATION, db_scenario)
        xml, errors = xml_builder.main_build_xml()
        if test_XML:
            return {"generated_xml": xml, "errors_count": len(errors), "errors": errors}
        elif len(errors) > 0:
            raise MissingPerrenoudDataException(
                errors_count=len(errors),
                errors=errors,
                scenario_name=db_scenario.name,
                is_initial_state=db_scenario.is_initial_state,
            )
        perrenoud_response = ScenarioService.send_perrenoud_request(xml)
        try:
            changes = PerrenoudParser.parse_xml(perrenoud_response)
        except:
            logging.error(f"PERRENOUD PARSING ERROR. INPUT_XML : {xml}")
            logging.error(f"PERRENOUD PARSING ERROR. OUTPUT_XML : {perrenoud_response}")
            raise PerrenoudWebserviceException()
        updated_scenario = ScenarioService.update(db_scenario, changes)
        return updated_scenario

    @staticmethod
    def get_new_scenario_name(base_scenario) -> str:
        number_scenarios = base_scenario.accommodation.scenarios_number
        if base_scenario.is_initial_state:
            return f"Scenario {number_scenarios+1}"
        else:
            return f"Copie - {base_scenario.name}"

    @staticmethod
    def send_perrenoud_request(xml):
        """Send Perrenoud request and return the response"""
        declaration = '<?xml version="1.0" encoding="UTF-8"?>'
        data = f"{declaration}{xml}"
        url = AppConfigService.get_by_key("perrenoud_url").value
        headers = {"Content-Type": "application/xml"}
        return requests.post(url, data=data.encode("utf-8"), headers=headers).text
