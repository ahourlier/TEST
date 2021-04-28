from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.hot_waters import HotWater
from app.perrenoud.hot_waters.error_handlers import HotWaterNotFoundException
from app.perrenoud.hot_waters.interface import HotWaterInterface


class HotWaterService:
    @staticmethod
    def get_by_id(hot_water_id: str) -> HotWater:
        db_hot_water = HotWater.query.get(hot_water_id)
        if db_hot_water is None:
            raise HotWaterNotFoundException
        return db_hot_water

    @staticmethod
    def create(new_attrs: HotWaterInterface, scenario_id=None, commit=True) -> HotWater:
        """ Create a new hot_water entity associated to a custom_field"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        hot_water = HotWater(**new_attrs)
        db.session.add(hot_water)
        if commit:
            db.session.commit()
        return hot_water

    @staticmethod
    def update(
        hot_water: HotWater, changes: HotWaterInterface, force_update: bool = False
    ) -> HotWater:
        if force_update or HotWaterService.has_changed(hot_water, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != hot_water.id:
                raise InconsistentUpdateIdException()
            hot_water.update(changes)
            db.session.commit()
        return hot_water

    @staticmethod
    def has_changed(hot_water: HotWater, changes: HotWaterInterface) -> bool:
        for key, value in changes.items():
            if getattr(hot_water, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(hot_water_id: int) -> int or None:
        hot_water = HotWater.query.filter(HotWater.id == hot_water_id).first()
        if not hot_water:
            raise HotWaterNotFoundException
        db.session.delete(hot_water)
        db.session.commit()
        return hot_water_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_hot_waters_id = [value.id for value in scenario.hot_waters]
        changes_hot_waters_id = [
            hot_waters_fields["id"]
            for hot_waters_fields in changes
            if "id" in hot_waters_fields
        ]

        for hot_water_fields in changes:
            # Create
            if "id" not in hot_water_fields:
                HotWaterService.create(hot_water_fields.copy(), scenario_id)
            # Update
            else:
                hot_water = HotWaterService.get_by_id(hot_water_fields["id"])
                HotWaterService.update(hot_water, hot_water_fields.copy())

        # Delete obsolete heatings
        for original_id in original_hot_waters_id:
            if original_id not in changes_hot_waters_id:
                HotWaterService.delete_by_id(original_id)

        return scenario.hot_waters

    @staticmethod
    def duplicate(base_hot_water, clone_scenario_parent_id):
        """ Duplicate an hot_water"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_hot_water, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_hot_water = HotWaterService.create(base_fields)
        db.session.flush()
        return clone_hot_water

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        hot_waters_id_map = {}
        for hot_water in base_scenario.hot_waters:
            clone_hot_water = HotWaterService.duplicate(hot_water, clone_scenario.id)
            hot_waters_id_map[hot_water.id] = clone_hot_water.id
        return hot_waters_id_map
