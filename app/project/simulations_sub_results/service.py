from app import db
from app.common.services_utils import ServicesUtils
from app.project.simulations.model import SimulationSubResult
import app.project.simulations.service as simulations_service
import app.project.accommodations.service as accommodations_service
from app.project.simulations_sub_results.error_handlers import (
    SimulationSubResultNotFoundException,
)


class SimulationSubResultService:
    @staticmethod
    def create(simulation_id: str, new_attrs) -> SimulationSubResult:
        """
        Create a new SimulationSubResult relationship
        """
        print("create sub result")
        ServicesUtils.clean_attrs(new_attrs, ["simulation"])
        simulations_service.SimulationService.get_by_id(simulation_id)
        if "accommodation" in new_attrs:
            accommodation = accommodations_service.AccommodationService.get_by_id(
                new_attrs.get("accommodation")["id"]
            )
            new_attrs["accommodation_id"] = accommodation.id
            ServicesUtils.clean_attrs(new_attrs, ["accommodation"])

        new_attrs["simulation_id"] = simulation_id

        simulation_sub_result = SimulationSubResult(**new_attrs)
        db.session.add(simulation_sub_result)
        db.session.commit()
        return simulation_sub_result

    @staticmethod
    def update(
        simulation_sub_result: SimulationSubResult,
        changes,
        force_update: bool = False,
    ) -> SimulationSubResult:
        ServicesUtils.clean_attrs(
            changes,
            [
                "accommodation",
                "simulation",
            ],
        )
        if force_update or SimulationSubResultService.has_changed(
            simulation_sub_result, changes
        ):
            if "accommodation" in changes:
                accommodation = accommodations_service.AccommodationService.get_by_id(
                    changes.get("accommodation")["id"]
                )
                changes["accommodation_id"] = accommodation.id
            simulation_sub_result.update(changes)
            db.session.commit()
        return simulation_sub_result

    @staticmethod
    def create_update_list(
        simulations_sub_results_fields,
        simulation_id,
    ):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        original_simulation_sub_results_id = [
            simulation_sub_result.id for simulation_sub_result in simulation.sub_results
        ]
        changes_ssr_id = [
            simulation_sub_result_field["id"]
            for simulation_sub_result_field in simulations_sub_results_fields
            if "id" in simulation_sub_result_field
        ]

        for simulation_sub_result_field in simulations_sub_results_fields:
            # Create
            if "id" not in simulation_sub_result_field:
                SimulationSubResultService.create(
                    simulation_id, simulation_sub_result_field.copy()
                )
            # Update
            else:
                sub_result = SimulationSubResultService.get_by_id(
                    simulation_sub_result_field["id"]
                )
                SimulationSubResultService.update(
                    sub_result,
                    simulation_sub_result_field.copy(),
                )

        # Delete obsolete simulations associations
        for original_id in original_simulation_sub_results_id:
            if original_id not in changes_ssr_id:
                SimulationSubResultService.delete_by_id(original_id)

        return simulation.sub_results

    @staticmethod
    def get_by_id(sub_result_id: str) -> SimulationSubResult:
        db_sub_result = SimulationSubResult.query.get(sub_result_id)
        if db_sub_result is None:
            raise SimulationSubResultNotFoundException()
        return db_sub_result

    @staticmethod
    def has_changed(sub_result: SimulationSubResult, changes) -> bool:
        for key, value in changes.items():
            if getattr(sub_result, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(sub_result_id: int) -> int or None:
        q = SimulationSubResult.query.filter_by(id=sub_result_id)
        if not q.scalar():
            raise SimulationSubResultNotFoundException()
        q.delete()
        db.session.commit()
        return sub_result_id

    @staticmethod
    def duplicate_sub_results(
        source_simulation_id: int,
        new_simulation_id: int,
    ):
        """
        Duplicate all sub_results from a simulation to another
        """
        source_simulation = simulations_service.SimulationService.get_by_id(
            source_simulation_id
        )
        new_simulation = simulations_service.SimulationService.get_by_id(
            new_simulation_id
        )
        for sub_result in source_simulation.sub_results:
            args = {
                "accommodation_id": sub_result.accommodation_id,
                "work_price": sub_result.work_price,
                "total_subvention": sub_result.total_subvention,
                "remaining_cost": sub_result.remaining_cost,
                "subvention_on_TTC": sub_result.subvention_on_TTC,
                "is_common_area": sub_result.is_common_area,
            }
            SimulationSubResultService.create(new_simulation_id, args)

        return new_simulation_id
