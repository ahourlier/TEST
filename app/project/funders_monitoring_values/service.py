from flask_sqlalchemy import Pagination

from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.common.services_utils import ServicesUtils
from app.project.funders_monitoring_values import FunderMonitoringValue, api
from app.project.funders_monitoring_values.exceptions import (
    FunderMonitoringValueNotFoundException,
)
from app.project.funders_monitoring_values.interface import (
    FunderMonitoringValueInterface,
)
import app.project.projects.service as projects_service
import app.mission.monitors.service as monitors_service
import app.funder.funders.service as funders_service
import app.project.comments.service as comments_service
import app.project.simulations.service as simulations_service
from app.project.comments.service import (
    FUNDER_ADVANCE_DATE_UPDATE,
    FUNDER_DEPOSIT_DATE_UPDATE,
    FUNDER_PAYMENT_DATE_UPDATE,
)


class FunderMonitoringValueService:
    @staticmethod
    def create(
        new_attrs: FunderMonitoringValueInterface, skip_unicity_check: bool = False
    ) -> FunderMonitoringValue:

        project = projects_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        funder = funders_service.FunderService.get_by_id(new_attrs.get("funder_id"))
        monitor_field = monitors_service.MonitorFieldService.get_by_id(
            new_attrs.get("monitor_field_id")
        )
        if skip_unicity_check is False:
            # Search for an existing funder_monitoring_value for the provided funder_id and with the
            # monitor_field value.
            funder_monitoring_value = (
                FunderMonitoringValue.query.filter(
                    FunderMonitoringValue.project_id == project.id
                )
                .filter(FunderMonitoringValue.monitor_field_id == monitor_field.id)
                .filter(FunderMonitoringValue.funder_id == funder.id)
                .first()
            )
            if funder_monitoring_value:
                # An existing value exist. The new funder_monitoring_value must not be created
                api.logger.error(
                    "A funder_monitoring_value already exists for this project, funder and monitor_field"
                )
                return None

        new_funder_monitoring_value = FunderMonitoringValue(**new_attrs)
        db.session.add(new_funder_monitoring_value)
        db.session.commit()
        return new_funder_monitoring_value

    @staticmethod
    def get_by_id(funder_monitoring_value_id: str) -> FunderMonitoringValue:
        db_funder_monitoring_value = FunderMonitoringValue.query.get(
            funder_monitoring_value_id
        )
        if db_funder_monitoring_value is None:
            raise FunderMonitoringValueNotFoundException
        return db_funder_monitoring_value

    @staticmethod
    def update(
        funder_monitoring_value: FunderMonitoringValue,
        changes: FunderMonitoringValueInterface,
    ) -> FunderMonitoringValue:

        # If one tries to update entity id, a error must be raised
        if changes.get("id") and changes.get("id") != funder_monitoring_value.id:
            raise InconsistentUpdateIdException()
        ServicesUtils.clean_attrs(
            changes, ["project_id", "funder_id", "monitor_field_id"]
        )

        if (
            funder_monitoring_value.monitor_field.name == "Avance"
            and "value" in changes
            and funder_monitoring_value.value != changes.get("value")
        ):
            comments_service.AutomaticCommentService.automatic_funder_comment(
                FUNDER_ADVANCE_DATE_UPDATE,
                funder_monitoring_value.funder.name,
                funder_monitoring_value.project,
            )
        if (
            (
                funder_monitoring_value.monitor_field.name == "Acompte 1"
                or funder_monitoring_value.monitor_field.name == "Acompte 2"
            )
            and "value" in changes
            and funder_monitoring_value.value != changes.get("value")
        ):
            comments_service.AutomaticCommentService.automatic_funder_comment(
                FUNDER_DEPOSIT_DATE_UPDATE,
                funder_monitoring_value.funder.name,
                funder_monitoring_value.project,
            )
        if (
            funder_monitoring_value.monitor_field.name == "Paiement du solde"
            and "value" in changes
            and funder_monitoring_value.value != changes.get("value")
        ):
            comments_service.AutomaticCommentService.automatic_funder_comment(
                FUNDER_PAYMENT_DATE_UPDATE,
                funder_monitoring_value.funder.name,
                funder_monitoring_value.project,
            )

        funder_monitoring_value.update(changes)
        db.session.commit()
        return funder_monitoring_value

    @staticmethod
    def update_list(project_id, payload):
        for funder_item in payload:
            for funder_monitoring_value_item in funder_item["fields"]:
                if (
                    "id" not in funder_monitoring_value_item
                    or "value" not in funder_monitoring_value_item
                ):
                    continue
                funder_monitoring_value = FunderMonitoringValueService.get_by_id(
                    funder_monitoring_value_item.get("id")
                )
                FunderMonitoringValueService.update(
                    funder_monitoring_value,
                    {"value": funder_monitoring_value_item.get("value")},
                )

        return FunderMonitoringValueService.fetch_project_fields_funders(project_id)

    @staticmethod
    def delete_by_id(funder_monitoring_value_id: int) -> int or None:
        funder_monitoring_value = FunderMonitoringValueService.get_by_id(
            funder_monitoring_value_id
        )
        db.session.delete(funder_monitoring_value)
        db.session.commit()
        return funder_monitoring_value_id

    @staticmethod
    def delete_by_monitor_field(monitor_field_id):
        # Delete all funding monitoring values for the provided monitor field id
        FunderMonitoringValue.query.filter(
            FunderMonitoringValue.monitor_field_id == monitor_field_id
        ).delete()
        db.session.commit()

    @staticmethod
    def fetch_project_fields_funders(project_id):
        """
        For one project, check all fields sorted by funder.
        If one funder_monitoring_field does not exist yet, creates it.
        Retrieve the list.
        """
        funders_items_list = []

        project = projects_service.ProjectService.get_by_id(project_id)
        # We call the "get_by_mission_id" method (and not just mission.monitor),
        # because we want the call to create the monitor if it does not exist yet
        monitor = monitors_service.MonitorService.get_by_mission_id(project.mission.id)

        simulations: Pagination = simulations_service.SimulationService.get_all(project_id=project_id)

        q_project_level = FunderMonitoringValue.query.filter(
            FunderMonitoringValue.project_id == project.id
        )

        funders_id = []

        # We get base funders from project simulations
        for simulation in simulations.items:
            # If simulation does not have any use case ("Dépot", "Dossier agréé", "Paiement")
            # we ignore its funders
            if not simulation.use_cases:
                continue

            for simulation_funder in simulation.base_funders:
                funder = simulation_funder.get("funder")
                funder_already_added = funder.id in funders_id
                if funder.is_deleted or funder_already_added:
                    # We do no fetch fields for deleted funder
                    # We also ignore funder already added
                    # No need to check if funder is duplicate
                    # because we are iterating only base funders from simulation
                    continue
                
                funders_id.append(funder.id)
                funder_item = {"funder": funder}
                funder_monitoring_values = []

                FMV_by_funder = q_project_level.filter(
                    FunderMonitoringValue.funder_id == funder.id
                ).all()
                funders_fields = {
                    FMV.monitor_field.id: ind for ind, FMV in enumerate(FMV_by_funder)
                }

                for field in monitor.fields:
                    if field.id in funders_fields:
                        # The monitoring value already exist so we append it to the list
                        monitoring_value_index = funders_fields[field.id]
                        funder_monitoring_values.append(
                            FMV_by_funder[monitoring_value_index]
                        )
                    else:
                        # The monitoring value does not exist so we create it
                        new_funder_monitoring_value = {
                            "monitor_field_id": field.id,
                            "project_id": project_id,
                            "funder_id": funder.id,
                            "date_value": None,
                            "boolean_value": None,
                        }
                        # We can skip the "unicity check" during the new funder_monitoring_value creation,
                        # because the above filter have already checked it.
                        funder_monitoring_value = FunderMonitoringValueService.create(
                            new_funder_monitoring_value, skip_unicity_check=True
                        )
                        funder_monitoring_values.append(funder_monitoring_value)

                funder_item["fields"] = funder_monitoring_values
                funders_items_list.append(funder_item)

        return funders_items_list
