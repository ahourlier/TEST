from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.ceilings import Ceiling
from app.perrenoud.ceilings.exceptions import CeilingNotFoundException
from app.perrenoud.ceilings.interface import CeilingInterface


class CeilingService:
    @staticmethod
    def get_by_id(ceiling_id: str) -> Ceiling:
        db_ceiling = Ceiling.query.get(ceiling_id)
        if db_ceiling is None:
            raise CeilingNotFoundException
        return db_ceiling

    @staticmethod
    def create(new_attrs: CeilingInterface, scenario_id=None, commit=True) -> Ceiling:
        """ Create a new ceiling"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        ceiling = Ceiling(**new_attrs)
        db.session.add(ceiling)
        if commit:
            db.session.commit()
        return ceiling

    @staticmethod
    def update(
        ceiling: Ceiling, changes: CeilingInterface, force_update: bool = False
    ) -> Ceiling:
        if force_update or CeilingService.has_changed(ceiling, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != ceiling.id:
                raise InconsistentUpdateIdException()
            ceiling.update(changes)
            db.session.commit()
        return ceiling

    @staticmethod
    def has_changed(ceiling: Ceiling, changes: CeilingInterface) -> bool:
        for key, value in changes.items():
            if getattr(ceiling, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(ceiling_id: int) -> int or None:
        ceiling = Ceiling.query.filter(Ceiling.id == ceiling_id).first()
        if not ceiling:
            raise CeilingNotFoundException
        db.session.delete(ceiling)
        db.session.commit()
        return ceiling_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_ceilings_id = [value.id for value in scenario.ceilings]
        changes_ceilings_id = [
            ceilings_fields["id"]
            for ceilings_fields in changes
            if "id" in ceilings_fields
        ]

        for ceiling_fields in changes:
            # Create
            if "id" not in ceiling_fields:
                CeilingService.create(ceiling_fields.copy(), scenario_id)
            # Update
            else:
                ceiling = CeilingService.get_by_id(ceiling_fields["id"])
                CeilingService.update(ceiling, ceiling_fields.copy())

        # Delete obsolete ceilings
        for original_id in original_ceilings_id:
            if original_id not in changes_ceilings_id:
                CeilingService.delete_by_id(original_id)

        return scenario.ceilings

    @staticmethod
    def duplicate(base_ceiling, clone_scenario_parent_id):
        """ Duplicate a ceiling"""
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_ceiling, extra_fields_to_remove=fields_to_treat_separately.copy()
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_ceiling = CeilingService.create(base_fields, commit=False)
        db.session.flush()
        return clone_ceiling

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        ceilings_id_map = {}
        for ceiling in base_scenario.ceilings:
            clone_ceiling = CeilingService.duplicate(ceiling, clone_scenario.id)
            ceilings_id_map[ceiling.id] = clone_ceiling.id
        return ceilings_id_map
