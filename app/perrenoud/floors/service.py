from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.floors import Floor
from app.perrenoud.floors.exceptions import FloorNotFoundException
from app.perrenoud.floors.interface import FloorInterface


class FloorService:
    @staticmethod
    def get_by_id(floor_id: str) -> Floor:
        db_floor = Floor.query.get(floor_id)
        if db_floor is None:
            raise FloorNotFoundException
        return db_floor

    @staticmethod
    def create(new_attrs: FloorInterface, scenario_id=None, commit=True) -> Floor:
        """ Create a new floor"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        floor = Floor(**new_attrs)
        db.session.add(floor)
        if commit:
            db.session.commit()
        return floor

    @staticmethod
    def update(
        floor: Floor, changes: FloorInterface, force_update: bool = False
    ) -> Floor:
        if force_update or FloorService.has_changed(floor, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != floor.id:
                raise InconsistentUpdateIdException()
            floor.update(changes)
            db.session.commit()
        return floor

    @staticmethod
    def has_changed(floor: Floor, changes: FloorInterface) -> bool:
        for key, value in changes.items():
            if getattr(floor, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(floor_id: int) -> int or None:
        floor = Floor.query.filter(Floor.id == floor_id).first()
        if not floor:
            raise FloorNotFoundException
        db.session.delete(floor)
        db.session.commit()
        return floor_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_floors_id = [value.id for value in scenario.floors]
        changes_floors_id = [
            floors_fields["id"] for floors_fields in changes if "id" in floors_fields
        ]

        for floor_fields in changes:
            # Create
            if "id" not in floor_fields:
                FloorService.create(floor_fields.copy(), scenario_id)
            # Update
            else:
                floor = FloorService.get_by_id(floor_fields["id"])
                FloorService.update(floor, floor_fields.copy())

        # Delete obsolete floors
        for original_id in original_floors_id:
            if original_id not in changes_floors_id:
                FloorService.delete_by_id(original_id)

        return scenario.floors

    @staticmethod
    def duplicate(base_floor, clone_scenario_parent_id):
        """ Duplicate a floor"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_floor, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_cloor = FloorService.create(base_fields, commit=False)
        db.session.flush()
        return clone_cloor

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        floors_id_map = {}
        for floor in base_scenario.floors:
            clone_floor = FloorService.duplicate(floor, clone_scenario.id)
            floors_id_map[floor.id] = clone_floor.id
        return floors_id_map
