from typing import List
from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
from app.common.services_utils import ServicesUtils
from app.perrenoud.heatings import Heating
from app.perrenoud.heatings.exceptions import HeatingNotFoundException
from app.perrenoud.heatings.interface import HeatingInterface
import app.perrenoud.scenarios.service as scenarios_service


class HeatingService:
    @staticmethod
    def get_by_id(heating_id: str) -> Heating:
        db_heating = Heating.query.get(heating_id)
        if db_heating is None:
            raise HeatingNotFoundException
        return db_heating

    @staticmethod
    def create(new_attrs: HeatingInterface, scenario_id=None, commit=True) -> Heating:
        """ Create a new heating"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        heating = Heating(**new_attrs)
        db.session.add(heating)
        if commit:
            db.session.commit()
        return heating

    @staticmethod
    def update(
        heating: Heating, changes: HeatingInterface, force_update: bool = False
    ) -> Heating:
        if force_update or HeatingService.has_changed(heating, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != heating.id:
                raise InconsistentUpdateIdException()
            heating.update(changes)
            db.session.commit()
        return heating

    @staticmethod
    def has_changed(heating: Heating, changes: HeatingInterface) -> bool:
        for key, value in changes.items():
            if getattr(heating, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(heating_id: int) -> int or None:
        heating = Heating.query.filter(Heating.id == heating_id).first()
        if not heating:
            raise HeatingNotFoundException

        alternative_heating = (
            Heating.query.filter(Heating.scenario_id == heating.scenario_id)
            .filter(Heating.id != heating_id)
            .first()
        )
        for room in heating.rooms:
            room.heating = alternative_heating
        db.session.delete(heating)
        db.session.commit()
        return heating_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_heatings_id = [value.id for value in scenario.heatings]
        changes_heatings_id = [
            heatings_fields["id"]
            for heatings_fields in changes
            if "id" in heatings_fields
        ]

        for heating_fields in changes:
            # Create
            if "id" not in heating_fields:
                HeatingService.create(heating_fields.copy(), scenario_id)
            # Update
            else:
                heating = HeatingService.get_by_id(heating_fields["id"])
                HeatingService.update(heating, heating_fields.copy())

        # Delete obsolete heatings
        for original_id in original_heatings_id:
            if original_id not in changes_heatings_id:
                HeatingService.delete_by_id(original_id)

        return scenario.heatings

    @staticmethod
    def duplicate(base_heating, clone_scenario_parent_id):
        """ Duplicate a heating"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_heating, extra_fields_to_remove=fields_to_treat_separately
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_heating = HeatingService.create(base_fields, commit=False)
        db.session.flush()
        return clone_heating

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        heatings_id_map = {}
        for heating in list(base_scenario.heatings):
            clone_heating = HeatingService.duplicate(heating, clone_scenario.id)
            heatings_id_map[heating.id] = clone_heating.id
        return heatings_id_map
