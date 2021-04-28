from typing import List

from app.admin.error_handlers import InconsistentUpdateIdException
from app import db
import app.perrenoud.scenarios.service as scenarios_service
from app.common.services_utils import ServicesUtils
from app.perrenoud.thermal_bridges import ThermalBridge
from app.perrenoud.thermal_bridges.exceptions import ThermalBridgeNotFoundException
from app.perrenoud.thermal_bridges.interface import ThermalBridgeInterface


class ThermalBridgeService:
    @staticmethod
    def get_by_id(thermal_bridge_id: str) -> ThermalBridge:
        db_thermal_bridge = ThermalBridge.query.get(thermal_bridge_id)
        if db_thermal_bridge is None:
            raise ThermalBridgeNotFoundException
        return db_thermal_bridge

    @staticmethod
    def create(
        new_attrs: ThermalBridgeInterface, scenario_id=None, commit=True
    ) -> ThermalBridge:
        """ Create a new thermal_bridge"""
        if scenario_id is not None:
            new_attrs["scenario_id"] = scenario_id
        scenarios_service.ScenarioService.get_by_id(new_attrs.get("scenario_id"))
        thermal_bridge = ThermalBridge(**new_attrs)
        db.session.add(thermal_bridge)
        if commit:
            db.session.commit()
        return thermal_bridge

    @staticmethod
    def update(
        thermal_bridge: ThermalBridge,
        changes: ThermalBridgeInterface,
        force_update: bool = False,
    ) -> ThermalBridge:
        if force_update or ThermalBridgeService.has_changed(thermal_bridge, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != thermal_bridge.id:
                raise InconsistentUpdateIdException()
            thermal_bridge.update(changes)
            db.session.commit()
        return thermal_bridge

    @staticmethod
    def has_changed(
        thermal_bridge: ThermalBridge, changes: ThermalBridgeInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(thermal_bridge, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(thermal_bridge_id: int) -> int or None:
        thermal_bridge = ThermalBridge.query.filter(
            ThermalBridge.id == thermal_bridge_id
        ).first()
        if not thermal_bridge:
            raise ThermalBridgeNotFoundException
        db.session.delete(thermal_bridge)
        db.session.commit()
        return thermal_bridge_id

    @staticmethod
    def create_update_list(scenario_id, changes: List):
        scenario = scenarios_service.ScenarioService.get_by_id(scenario_id)
        original_thermal_bridges_id = [value.id for value in scenario.thermal_bridges]
        changes_thermal_bridges_id = [
            thermal_bridges_fields["id"]
            for thermal_bridges_fields in changes
            if "id" in thermal_bridges_fields
        ]

        for thermal_bridge_fields in changes:
            # Create
            if "id" not in thermal_bridge_fields:
                ThermalBridgeService.create(thermal_bridge_fields.copy(), scenario_id)
            # Update
            else:
                thermal_bridge = ThermalBridgeService.get_by_id(
                    thermal_bridge_fields["id"]
                )
                ThermalBridgeService.update(
                    thermal_bridge, thermal_bridge_fields.copy()
                )

        # Delete obsolete available_field_values
        for original_id in original_thermal_bridges_id:
            if original_id not in changes_thermal_bridges_id:
                ThermalBridgeService.delete_by_id(original_id)

        return scenario.thermal_bridges

    @staticmethod
    def duplicate(base_thermal_bridge, clone_scenario_parent_id):
        """ Duplicate a thermal_bridge """
        fields_to_treat_separately = ["scenario_id"]
        base_fields = ServicesUtils.fetch_dict_fields_from_object(
            base_thermal_bridge,
            extra_fields_to_remove=fields_to_treat_separately.copy(),
        )
        base_fields["scenario_id"] = clone_scenario_parent_id
        clone_thermal_bridge = ThermalBridgeService.create(base_fields, commit=False)
        db.session.commit()
        return clone_thermal_bridge

    @staticmethod
    def duplicate_all_from_scenarios(base_scenario, clone_scenario):
        thermal_bridges_id_map = {}
        for thermal_bridge in base_scenario.thermal_bridges:
            clone_thermal_bridge = ThermalBridgeService.duplicate(
                thermal_bridge, clone_scenario.id
            )
            thermal_bridges_id_map[thermal_bridge.id] = clone_thermal_bridge.id
        return thermal_bridges_id_map
