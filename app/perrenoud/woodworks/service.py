from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.woodworks import Woodwork
from app.perrenoud.woodworks.exceptions import WoodworkNotFoundException
from app.perrenoud.woodworks.interface import WoodworkInterface


class WoodworkService:
    @staticmethod
    def get_by_id(woodwork_id: str) -> Woodwork:
        db_woodwork = Woodwork.query.get(woodwork_id)
        if db_woodwork is None:
            raise WoodworkNotFoundException
        return db_woodwork

    @staticmethod
    def create(new_attrs: WoodworkInterface, scenario_id=None, commit=True) -> Woodwork:
        """Create a new woodwork"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        woodwork = Woodwork(**new_attrs)
        db.session.add(woodwork)
        if commit:
            db.session.commit()
        return woodwork

    @staticmethod
    def update(
        woodwork: Woodwork, changes: WoodworkInterface, force_update: bool = False
    ) -> Woodwork:
        if force_update or WoodworkService.has_changed(woodwork, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != woodwork.id:
                raise InconsistentUpdateIdException()
            woodwork.update(changes)
            db.session.commit()
        return woodwork

    @staticmethod
    def has_changed(woodwork: Woodwork, changes: WoodworkInterface) -> bool:
        for key, value in changes.items():
            if getattr(woodwork, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(woodwork_id: int) -> int or None:
        woodwork = Woodwork.query.filter(Woodwork.id == woodwork_id).first()
        if not woodwork:
            raise WoodworkNotFoundException
        db.session.delete(woodwork)
        db.session.commit()
        return woodwork_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_woodworks_id = [value.id for value in scenario.woodworks]
        changes_woodworks_id = [
            woodworks_fields["id"]
            for woodworks_fields in changes
            if "id" in woodworks_fields
        ]

        for woodwork_fields in changes:
            # Create
            if "id" not in woodwork_fields:
                WoodworkService.create(woodwork_fields.copy(), scenario_id)
            # Update
            else:
                woodwork = WoodworkService.get_by_id(woodwork_fields["id"])
                WoodworkService.update(woodwork, woodwork_fields.copy())

        # Delete obsolete woodworks
        for original_id in original_woodworks_id:
            if original_id not in changes_woodworks_id:
                WoodworkService.delete_by_id(original_id)

        return scenario.woodworks

    @staticmethod
    def duplicate(base_woodwork, clone_scenario_parent_id):
        """Duplicate a woodwork"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_woodwork, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_woodwork = WoodworkService.create(base_fields, commit=False)
        db.session.flush()
        return clone_woodwork

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        woodworks_id_map = {}
        for woodwork in base_scenario.woodworks:
            clone_woodwork = WoodworkService.duplicate(woodwork, clone_scenario.id)
            woodworks_id_map[woodwork.id] = clone_woodwork.id
        return woodworks_id_map
