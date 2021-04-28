from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.walls import Wall
from app.perrenoud.walls.error_handlers import WallNotFoundException
from app.perrenoud.walls.interface import WallInterface


class WallService:
    @staticmethod
    def get_by_id(wall_id: str) -> Wall:
        db_wall = Wall.query.get(wall_id)
        if db_wall is None:
            raise WallNotFoundException
        return db_wall

    @staticmethod
    def create(new_attrs: WallInterface, scenario_id=None, commit=True) -> Wall:
        """ Create a new wall"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        wall = Wall(**new_attrs)
        db.session.add(wall)
        if commit:
            db.session.commit()
        return wall

    @staticmethod
    def update(wall: Wall, changes: WallInterface, force_update: bool = False) -> Wall:
        if force_update or WallService.has_changed(wall, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != wall.id:
                raise InconsistentUpdateIdException()
            wall.update(changes)
            db.session.commit()
        return wall

    @staticmethod
    def has_changed(wall: Wall, changes: WallInterface) -> bool:
        for key, value in changes.items():
            if getattr(wall, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(wall_id: int) -> int or None:
        wall = Wall.query.filter(Wall.id == wall_id).first()
        if not wall:
            raise WallNotFoundException
        db.session.delete(wall)
        db.session.commit()
        return wall_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_walls_id = [value.id for value in scenario.walls]
        changes_walls_id = [
            walls_fields["id"] for walls_fields in changes if "id" in walls_fields
        ]

        for wall_fields in changes:
            # Create
            if "id" not in wall_fields:
                WallService.create(wall_fields.copy(), scenario_id)
            # Update
            else:
                wall = WallService.get_by_id(wall_fields["id"])
                WallService.update(wall, wall_fields.copy())

        # Delete obsolete available_field_values
        for original_id in original_walls_id:
            if original_id not in changes_walls_id:
                WallService.delete_by_id(original_id)

        return scenario.walls

    @staticmethod
    def duplicate(base_wall, clone_scenario_parent_id):
        """ Duplicate a wall"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_wall, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_wall = WallService.create(base_fields, commit=False)
        db.session.flush()
        return clone_wall

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        walls_id_map = {}
        for wall in base_scenario.walls:
            clone_wall = WallService.duplicate(wall, clone_scenario.id)
            walls_id_map[wall.id] = clone_wall.id
        return walls_id_map
