from app import db
from app.project.simulations import Simulation
from app.project.simulations.model import SimulationAccommodation

import app.project.simulations.service as simulations_service
import app.project.accommodations.service as accommodations_service
from app.project.simulations_accommodations.error_handlers import (
    SimulationAccommodationNotFoundException,
    SimulationAlreadyUsedException,
)


class SimulationAccommodationService:
    @staticmethod
    def create(simulation_id: str, new_attrs) -> SimulationAccommodation:
        """
        Create a new SimulationAccommodation relationship
        """
        simulations_service.SimulationService.get_by_id(simulation_id)
        new_attrs["simulation_id"] = simulation_id
        accommodations_service.AccommodationService.get_by_id(
            new_attrs["accommodation"]["id"]
        )
        new_attrs["accommodation_id"] = new_attrs["accommodation"]["id"]
        del new_attrs["accommodation"]

        if SimulationAccommodationService.accommodation_already_used(
            simulation_id, new_attrs["accommodation_id"]
        ):
            raise SimulationAlreadyUsedException

        simulation_accommodation = SimulationAccommodation(**new_attrs)
        db.session.add(simulation_accommodation)
        db.session.commit()
        return simulation_accommodation

    @staticmethod
    def accommodation_already_used(simulation_id, accommodation_id):
        """Check if accommodation is already associated to a simulation"""
        q = Simulation.query.filter(Simulation.id == simulation_id).filter(
            Simulation.simulations_accommodations.any(
                SimulationAccommodation.accommodation_id == accommodation_id
            )
        )
        return q.scalar() is not None

    @staticmethod
    def update(
        simulation_accommodation: SimulationAccommodation,
        changes,
        force_update: bool = False,
    ) -> SimulationAccommodation:
        # Remove "accommodation" key. We don't update that.
        if "accommodation" in changes:
            del changes["accommodation"]
        if force_update or SimulationAccommodationService.has_changed(
            simulation_accommodation, changes
        ):
            simulation_accommodation.update(changes)
            db.session.commit()
        return simulation_accommodation

    @staticmethod
    def create_update_list(simulations_accommodations_fields, simulation_id):
        simulation = simulations_service.SimulationService.get_by_id(simulation_id)
        original_simulations_id = [
            simulation_accommodation.id
            for simulation_accommodation in simulation.simulations_accommodations
        ]
        changes_sa_id = [
            simulation_accommodation_field["id"]
            for simulation_accommodation_field in simulations_accommodations_fields
            if "id" in simulation_accommodation_field
        ]

        for simulation_accommodation_field in simulations_accommodations_fields:
            # Create
            if "id" not in simulation_accommodation_field:
                SimulationAccommodationService.create(
                    simulation_id, simulation_accommodation_field.copy()
                )
            # Update
            else:
                simulation_accommodation = SimulationAccommodationService.get_by_id(
                    simulation_accommodation_field["id"]
                )
                SimulationAccommodationService.update(
                    simulation_accommodation, simulation_accommodation_field.copy()
                )

        # Delete obsolete simulations associations
        for original_id in original_simulations_id:
            if original_id not in changes_sa_id:
                SimulationAccommodationService.delete_by_id(original_id)

        return simulation.simulations_accommodations

    @staticmethod
    def get_by_id(simulation_accommodation_id: str) -> SimulationAccommodation:
        db_simulation_accommodation = SimulationAccommodation.query.get(
            simulation_accommodation_id
        )
        if db_simulation_accommodation is None:
            raise SimulationAccommodationNotFoundException()
        return db_simulation_accommodation

    @staticmethod
    def has_changed(simulation_accommodation: SimulationAccommodation, changes) -> bool:
        for key, value in changes.items():
            if getattr(simulation_accommodation, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(simulation_accommodation_id: int) -> int or None:
        q = SimulationAccommodation.query.filter_by(id=simulation_accommodation_id)
        if not q.scalar():
            raise SimulationAccommodationNotFoundException
        q.delete()
        db.session.commit()
        return simulation_accommodation_id

    @staticmethod
    def duplicate_simulations_accommodations(
        source_simulation_id: int, new_simulation_id: int
    ) -> Simulation:
        """
        Duplicate all simulations_accommodations from a simulation to another
        """

        source_simulation = simulations_service.SimulationService.get_by_id(
            source_simulation_id
        )
        new_simulation = simulations_service.SimulationService.get_by_id(
            new_simulation_id
        )

        for simulation_accommodation in source_simulation.simulations_accommodations:
            args = {
                "rent_type": simulation_accommodation.rent_type,
                "rent_per_msq": simulation_accommodation.rent_per_msq,
                "rent": simulation_accommodation.rent,
                "accommodation": {"id": simulation_accommodation.accommodation_id},
            }
            SimulationAccommodationService.create(new_simulation_id, args)

        return new_simulation
