from app import db
from app.common.services_utils import ServicesUtils
from app.project.funder_accommodations.exceptions import (
    FunderAccommodationsNotFoundException,
)
from app.project.simulations.model import FunderAccommodation, SimulationFunder

import app.project.simulations.service as simulations_service
import app.project.accommodations.service as accommodations_service
import app.funder.funding_scenarios.service as scenarios_service
import app.project.projects.service as projects_service


class FunderAccommodationService:
    @staticmethod
    def create(
        simulation_funder_id: str, new_attrs, reset_scenario: bool = True
    ) -> FunderAccommodation:
        """
        Create a new FunderAccommodation relationship
        """
        ServicesUtils.clean_attrs(new_attrs, ["scenario"])
        simulation_funder = simulations_service.SimulationFunderService.get_by_id(
            simulation_funder_id
        )
        if "accommodation" in new_attrs:
            accommodation = accommodations_service.AccommodationService.get_by_id(
                new_attrs.get("accommodation")["id"]
            )
            new_attrs["accommodation_id"] = accommodation.id
            ServicesUtils.clean_attrs(new_attrs, ["accommodation"])

        if reset_scenario:
            quotes_id = [
                simulation_quote.base_quote_id
                for simulation_quote in simulation_funder.simulation.simulation_quotes
            ]
            scenario = scenarios_service.FundingScenarioService.get_match_scenarios(
                simulation_funder.duplicate_funder,
                simulation_funder.simulation.project_id,
                new_attrs.get("accommodation_id"),
                quotes_id=quotes_id,
            )
            new_attrs["scenario_id"] = scenario.id if scenario is not None else None
        else:
            scenarios_service.FundingScenarioService.get_by_id(
                new_attrs.get("scenario_id")
            )
        new_attrs["simulation_funder_id"] = simulation_funder_id

        funder_accommodation = FunderAccommodation(**new_attrs)
        db.session.add(funder_accommodation)
        db.session.commit()
        return funder_accommodation

    @staticmethod
    def update(
        funder_accommodation: FunderAccommodation,
        changes,
        force_update: bool = False,
        reset_scenario: bool = False,
    ) -> FunderAccommodation:
        ServicesUtils.clean_attrs(
            changes,
            ["accommodation", "scenario", "simulation_funder" "simulation_funder_id",],
        )
        if force_update or FunderAccommodationService.has_changed(
            funder_accommodation, changes
        ):
            if "accommodation" in changes:
                accommodation = accommodations_service.AccommodationService.get_by_id(
                    changes.get("accommodation")["id"]
                )
                changes["accommodation_id"] = accommodation.id
            if reset_scenario:
                quotes_id = [
                    simulation_quote.base_quote_id
                    for simulation_quote in funder_accommodation.simulation_funder.simulation.simulation_quotes
                ]
                scenario = scenarios_service.FundingScenarioService.get_match_scenarios(
                    funder_accommodation.simulation_funder.duplicate_funder,
                    funder_accommodation.simulation_funder.simulation.project_id,
                    changes.get("accommodation_id"),
                    quotes_id=quotes_id,
                )
                changes["scenario_id"] = scenario.id if scenario is not None else None

            funder_accommodation.update(changes)
            db.session.commit()
        return funder_accommodation

    @staticmethod
    def create_update_list(
        funders_accommodations_fields,
        simulation_funder_id,
        reset_scenario: bool = False,
    ):
        simulation_funder = simulations_service.SimulationFunderService.get_by_id(
            simulation_funder_id
        )
        original_simulation_funders_id = [
            funder_accommodation.id
            for funder_accommodation in simulation_funder.funder_accommodations
        ]
        changes_sf_id = [
            funder_accommodations_field["id"]
            for funder_accommodations_field in funders_accommodations_fields
            if "id" in funder_accommodations_field
        ]

        for funder_accommodations_fields in funders_accommodations_fields:
            # Create
            if "id" not in funder_accommodations_fields:
                FunderAccommodationService.create(
                    simulation_funder_id, funder_accommodations_fields.copy()
                )
            # Update
            else:
                funder_accommodation = FunderAccommodationService.get_by_id(
                    funder_accommodations_fields["id"]
                )
                FunderAccommodationService.update(
                    funder_accommodation,
                    funder_accommodations_fields.copy(),
                    reset_scenario=reset_scenario,
                )

        # Delete obsolete simulations associations
        for original_id in original_simulation_funders_id:
            if original_id not in changes_sf_id:
                FunderAccommodationService.delete_by_id(original_id)

        return simulation_funder.funder_accommodations

    @staticmethod
    def get_by_id(funder_accommodation_id: str) -> FunderAccommodation:
        db_funder_accommodation = FunderAccommodation.query.get(funder_accommodation_id)
        if db_funder_accommodation is None:
            raise FunderAccommodationsNotFoundException()
        return db_funder_accommodation

    @staticmethod
    def has_changed(funder_accommodation: FunderAccommodation, changes) -> bool:
        for key, value in changes.items():
            if getattr(funder_accommodation, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(funder_accommodation_id: int) -> int or None:
        q = FunderAccommodation.query.filter_by(id=funder_accommodation_id)
        if not q.scalar():
            raise FunderAccommodationsNotFoundException()
        q.delete()
        db.session.commit()
        return funder_accommodation_id

    @staticmethod
    def duplicate_funders_accommodations(
        source_simulation_funder_id: int, new_simulation_funder_id: int,
    ) -> SimulationFunder:
        """
        Duplicate all funders_accommodations from a simulation_funder to another
        """

        source_simulation_funder = simulations_service.SimulationFunderService.get_by_id(
            source_simulation_funder_id
        )
        new_simulation_funder = simulations_service.SimulationFunderService.get_by_id(
            new_simulation_funder_id
        )
        for funder_accommodations in source_simulation_funder.funder_accommodations:
            if not funder_accommodations.is_common_area:
                args = {
                    "rate": funder_accommodations.rate,
                    "subventioned_expense": funder_accommodations.subventioned_expense,
                    "is_common_area": funder_accommodations.is_common_area,
                    "accommodation_id": funder_accommodations.accommodation_id,
                    "scenario_id": funder_accommodations.scenario_id,
                }
            else:
                args = {
                    "rate": funder_accommodations.rate,
                    "subventioned_expense": funder_accommodations.subventioned_expense,
                    "is_common_area": funder_accommodations.is_common_area,
                }
            FunderAccommodationService.create(new_simulation_funder_id, args)

        return new_simulation_funder

    @staticmethod
    def construct_initial_funder_accommodations(
        base_funder=None,
        project_id=None,
        accommodations_id=[],
        quotes_id=[],
        common_scenario=None,
    ):
        if not common_scenario:
            common_scenario = scenarios_service.FundingScenarioService.get_match_scenarios(
                base_funder, project_id, quotes_id=quotes_id
            )
        funder_accommodations = []

        project = projects_service.ProjectService.get_by_id(project_id)
        common_area_surface = (
            0
            if project.common_areas is None or project.common_areas.area is None
            else project.common_areas.area
        )
        common_area = {
            "scenario": common_scenario,
            "rate": None,
            "subventioned_expense": None,
            "is_common_area": True,
            "common_area_surface": common_area_surface,
        }
        funder_accommodations.append(common_area)
        for accommodation_id in accommodations_id:
            accommodation = accommodations_service.AccommodationService.get_by_id(
                accommodation_id
            )
            scenario = scenarios_service.FundingScenarioService.get_match_scenarios(
                base_funder,
                project_id,
                quotes_id=quotes_id,
                accommodation_id=accommodation_id,
            )

            funder_accommodations.append(
                {
                    "accommodation": accommodation,
                    "scenario": scenario,
                    "rate": None,
                    "subventioned_expense": None,
                    "is_common_area": False,
                }
            )
        return funder_accommodations
