import json
from typing import List
import logging

# from flask import app
from flask import jsonify
from flask_sqlalchemy import Pagination

from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.common.services_utils import ServicesUtils
from app.mission.missions import Mission
from app.mission.monitors import Monitor, api
from app.mission.monitors.error_handlers import (
    MonitorNotFoundException,
    MonitorFieldNotFoundException,
)
from app.mission.monitors.interface import MonitorInterface, MonitorFieldInterface
import app.mission.missions.service as missions_service
from app.mission.monitors.model import MonitorField, DEFAULT_FIELDS
import app.project.funders_monitoring_values.service as funders_monitoring_values_service


class MonitorService:
    @staticmethod
    def create(new_attrs: MonitorInterface) -> Monitor:
        new_monitor = Monitor(**new_attrs)
        db.session.add(new_monitor)
        db.session.commit()
        MonitorFieldService.initialize_default_fields(new_monitor)
        return new_monitor

    @staticmethod
    def get_by_mission_id(mission_id):
        mission = missions_service.MissionService.get_by_id(mission_id)
        # Instantiate a new monitor if mission does not have one
        if not mission.monitor:
            new_monitor = {
                "mission_id": mission_id,
                "advance_alert": None,
                "payment_alert": None,
                "commentary": None,
            }
            MonitorService.create(new_monitor)
        return mission.monitor

    @staticmethod
    def get_by_id(monitor_id: str) -> Monitor:
        db_monitor = Monitor.query.get(monitor_id)
        if db_monitor is None:
            raise MonitorNotFoundException
        return db_monitor

    @staticmethod
    def update(monitor: Monitor, changes: MonitorInterface) -> Monitor:

        # If one tries to update entity id, a error must be raised
        if changes.get("id") and changes.get("id") != monitor.id:
            raise InconsistentUpdateIdException()
        extracted_fields = ServicesUtils.clean_attrs(changes, ["fields"])
        monitor.update(changes)
        db.session.commit()

        # Update children fields associated to the monitor
        if "fields" in extracted_fields:
            MonitorFieldService.create_update_list(
                monitor.id, extracted_fields["fields"]
            )
        return monitor


class MonitorFieldService:
    @staticmethod
    def create(
        new_attrs: MonitorFieldInterface, is_default: bool = False
    ) -> MonitorField:
        if is_default is False:
            # Non-default fields cannot be created as automatic or default
            new_attrs["automatic"] = False
            new_attrs["default"] = False

            # New fields are always dates
            new_attrs["type"] = "date"

        new_monitor_field = MonitorField(**new_attrs)
        db.session.add(new_monitor_field)
        db.session.commit()
        return new_monitor_field

    @staticmethod
    def initialize_default_fields(monitor: Monitor):
        default_fields = json.loads(DEFAULT_FIELDS)
        for field in default_fields:
            field["monitor_id"] = monitor.id
            MonitorFieldService.create(field, is_default=True)
        return monitor

    @staticmethod
    def get_by_id(monitor_field_id: str) -> MonitorField:
        db_monitor_field = MonitorField.query.get(monitor_field_id)
        if db_monitor_field is None:
            raise MonitorFieldNotFoundException
        return db_monitor_field

    @staticmethod
    def update(
        monitor_field: MonitorField,
        changes: MonitorFieldInterface,
        force_update: bool = False,
    ) -> MonitorField:
        if force_update or MonitorFieldService.has_changed(monitor_field, changes):

            # Clean changes:
            ServicesUtils.clean_attrs(changes, ["automatic", "type", "monitor_id"])

            if "default" in changes:
                if monitor_field.default is True:
                    changes = {"invisible": changes["invisible"]}
                else:
                    del changes["default"]

            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != monitor_field.id:
                raise InconsistentUpdateIdException()

            monitor_field.update(changes)
            db.session.commit()

    @staticmethod
    def has_changed(
        monitor_field: MonitorField, changes: MonitorFieldInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(monitor_field, key) != value:
                return True
        return False

    @staticmethod
    def create_update_list(monitor_id, changes: List):
        monitor = MonitorService.get_by_id(monitor_id)

        for monitor_field_value in changes:
            # Create
            if "id" not in monitor_field_value:
                monitor_field_value["monitor_id"] = monitor_id
                MonitorFieldService.create(monitor_field_value.copy())
            # Update
            else:
                monitor_field = MonitorFieldService.get_by_id(monitor_field_value["id"])
                MonitorFieldService.update(monitor_field, monitor_field_value.copy())
        return monitor.fields

    @staticmethod
    def delete_by_id(monitor_field_id: int, delete_default: bool = True) -> int or None:
        monitor_field = MonitorFieldService.get_by_id(monitor_field_id)
        if not monitor_field:
            raise MonitorFieldNotFoundException

        if delete_default is False and monitor_field.default is True:
            api.logger.error("This default monitoring field cannot be deleted")
            return jsonify(dict(status="Fail", id=monitor_field_id))
        else:
            funders_monitoring_values_service.FunderMonitoringValueService.delete_by_monitor_field(
                monitor_field.id
            )
            db.session.delete(monitor_field)
            db.session.commit()
            return jsonify(dict(status="Success", id=monitor_field_id))
