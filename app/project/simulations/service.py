import collections
from datetime import datetime
from typing import List

from flask import g
from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.common.exceptions import (
    InconsistentUpdateIdException,
    ForbiddenException,
    InvalidSearchFieldException,
    InvalidParamsRequestException,
)
from app.common.search import sort_query
from app.funder.funders import Funder
from app.funder.funding_scenarios import FundingScenario
from app.perrenoud.scenarios.service import ScenarioService
from app.project import simulations
from app.project.quotes.interface import QuoteInterface
from app.project.simulations import Simulation
from .error_handlers import (
    SimulationNotFoundException,
    UseCaseSimulationNotFoundException,
    SimulationUsedException,
    CloneFunderException,
    SimulationQuoteNotFoundException,
    SimulationFunderNotFoundException,
    InconsistentScenarioException
)
from app.project.simulations.interface import (
    SimulationInterface,
    SimulationUseCaseInterface,
    SimulationQuoteInterface,
    SimulationFunderInterface,
)
from app.project.simulations.model import (
    SimulationUseCase,
    SimulationQuote,
    SimulationFunder,
    SIMULATIONS_KEYWORD_SORT,
    SIMULATIONS_USE_CASES,
)

import app.funder.funders.service as funders_service
import app.project.projects.service as project_service
import app.project.quotes.service as quotes_service
import app.project.simulations_uses.service as simulation_uses_service
import app.funder.funding_scenarios.service as funding_scenario_service
import app.project.simulations_accommodations.service as simulations_accommodations_service
import app.project.funder_accommodations.service as funder_accommodations_service
import app.project.accommodations.service as accommodations_service
import app.project.simulations_sub_results.service as sub_resuts_service
from ..requesters.model import RequesterTypes
from ...common.services_utils import ServicesUtils

SIMULATIONS_DEFAULT_PAGE = 1
SIMULATIONS_DEFAULT_PAGE_SIZE = 100
SIMULATIONS_DEFAULT_SORT_FIELD = "created_at"
SIMULATIONS_DEFAULT_SORT_DIRECTION = "desc"


class SimulationService:
    @staticmethod
    def get_all(
        page=SIMULATIONS_DEFAULT_PAGE,
        size=SIMULATIONS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=SIMULATIONS_DEFAULT_SORT_FIELD,
        direction=SIMULATIONS_DEFAULT_SORT_DIRECTION,
        quote_id=None,
        funder_id=None,
        project_id=None,
        use_case=None,
    ) -> Pagination:
        q = sort_query(Simulation.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(or_(Simulation.name.ilike(search_term),))

        if quote_id is not None:
            q = q.filter(
                Simulation.simulation_quotes.any(
                    SimulationQuote.base_quote_id == quote_id
                )
            )
        if funder_id is not None:
            q = q.filter(
                Simulation.simulation_funders.any(
                    SimulationFunder.base_funder_id == funder_id
                )
            )
        if project_id is not None:
            q = q.filter(Simulation.project_id == project_id)

        # Filter on use case
        if use_case is not None and use_case not in SIMULATIONS_KEYWORD_SORT:
            raise InvalidSearchFieldException()
        if use_case is not None:
            q = q.filter(
                Simulation.use_cases.any(
                    SimulationUseCase.use_case_name
                    == SIMULATIONS_KEYWORD_SORT[use_case]
                )
            )
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(simulation_id: str) -> Simulation:
        db_simulation = Simulation.query.get(simulation_id)
        if db_simulation is None:
            raise SimulationNotFoundException
        return db_simulation

    @staticmethod
    def create(new_attrs: SimulationInterface) -> Simulation:
        """ Create a new simulation """

        # Verify parent project existence
        project_service.ProjectService.get_by_id(new_attrs["project_id"])
        extracted_fields = ServicesUtils.clean_attrs(
            new_attrs,
            [
                "sub_results",
                "use_cases",
                "quotes",
                "funders",
                "simulations_accommodations",
            ],
        )
        

        # Create new simulation
        simulation = Simulation(**new_attrs)
        db.session.add(simulation)
        db.session.commit()

        # Create childrens and more complex associations
        if "quotes" in extracted_fields:
            SimulationQuoteService.update_list(simulation, extracted_fields["quotes"])
        if "simulations_accommodations" in extracted_fields:
            simulations_accommodations_service.SimulationAccommodationService.create_update_list(
                extracted_fields["simulations_accommodations"], simulation.id
            )
        if "funders" in extracted_fields:
            SimulationFunderService.update_list(simulation, extracted_fields["funders"])
        if "use_cases" in extracted_fields:
            SimulationUseCaseService.create_list(
                extracted_fields["use_cases"], simulation.id
            )
        if "sub_results" in extracted_fields:
            sub_resuts_service.SimulationSubResultService.create_update_list(
                extracted_fields["sub_results"], simulation.id
            )

        return simulation

    @staticmethod
    def duplicate(simulation_id: str) -> Simulation:
        """
        Duplicate a simulation with his children quotes and simulations.
        Use_cases relations must no be duplicated
        """
        base_simulation = SimulationService.get_by_id(simulation_id)
        duplicate_dict = base_simulation.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(duplicate_dict):
            if key not in base_simulation.__table__.columns.keys():
                del duplicate_dict[key]
        # Remove auto_generated values :
        del duplicate_dict["id"]
        del duplicate_dict["updated_at"]
        del duplicate_dict["created_at"]
        duplicate_dict["name"] = f"Copie de {duplicate_dict['name']}"

        # Create new simulation
        duplicated_simulation = SimulationService.create(
            SimulationInterface(**duplicate_dict)
        )
        # Duplicate and assign cloned quotes to the new simulation :
        quotes_to_join = [
            simulation_quote.base_quote.id
            for simulation_quote in base_simulation.simulation_quotes
        ]
        SimulationQuoteService.create_by_quotes_id(
            {"quotes_id": quotes_to_join}, duplicated_simulation.id
        )

        # Duplicate accommodations relations :
        simulations_accommodations_service.SimulationAccommodationService.duplicate_simulations_accommodations(
            simulation_id, duplicated_simulation.id
        )
        # Duplicate simulation_funders
        SimulationFunderService.duplicate_simulation_funders(
            simulation_id, duplicated_simulation.id
        )
        # Duplicate sub_results
        sub_resuts_service.SimulationSubResultService.duplicate_sub_results(
            simulation_id, duplicated_simulation.id
        )

        return duplicated_simulation

    @staticmethod
    def update(
        simulation: Simulation, changes: SimulationInterface, force_update: bool = True
    ) -> Simulation:
        """ This update worflow is special due to a business rule :
        some fields cannot be modified since the simulation is "used" (frozen),
        while other can always be modified."""
        if force_update or SimulationService.has_changed(simulation, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != simulation.id:
                raise InconsistentUpdateIdException()

            # Every time a simulation is updated, his "quotes_modified" must be set as False.
            # Because we consider user has been informed of quotes_changes and accepted it
            changes["quotes_modified"] = False

            simulation_was_frozen = simulation.is_frozen
            # Update uses_cases :
            SimulationUseCaseService.update_list(
                changes.get("use_cases"), simulation.id
            )
            del changes["use_cases"]

            # If scenario_id, check if scenario is in the same project
            if changes.get("scenario_id"):
                existing_scenario = ScenarioService.get_by_id(changes.get("scenario_id"))
                if existing_scenario.accommodation.project_id != simulation.project_id:
                    raise InconsistentScenarioException

            # Update simulations_use notes :
            # (Notes can always be updated, even when simulation is "frozen")
            NOTES_FIELDS = [
                "note_certifications",
                "note_payment_requests",
                "note_deposits",
            ]
            notes_changes = {
                note: changes[note]
                for note in NOTES_FIELDS
                if note in changes and changes[note] != getattr(simulation, note, None)
            }
            simulation.update(notes_changes)
            db.session.commit()

            # After updating use_cases, check if simulation is still frozen AND if it was frozen initially :
            # (Because a simulation with uses cases cannot be updated):
            if simulation.is_frozen and simulation_was_frozen:
                return simulation

            # Update children and complex relationships
            if "quotes" in changes:
                SimulationQuoteService.update_list(simulation, changes["quotes"])
                del changes["quotes"]
            if "funders" in changes:
                SimulationFunderService.update_list(simulation, changes["funders"])
                del changes["funders"]
            if "simulations_accommodations" in changes:
                simulations_accommodations_service.SimulationAccommodationService.create_update_list(
                    changes.get("simulations_accommodations"), simulation.id
                )
                del changes["simulations_accommodations"]
            if "sub_results" in changes:
                sub_resuts_service.SimulationSubResultService.create_update_list(
                    changes.get("sub_results"), simulation.id
                )
                del changes["sub_results"]

            # Update simulation with the remaining changes values (only is use cases are empty)
            simulation.update(changes)
            db.session.commit()
        return simulation

    @staticmethod
    def has_changed(simulation: Simulation, changes: SimulationInterface) -> bool:
        for key, value in changes.items():
            if getattr(simulation, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(simulation_id: int) -> int or None:
        simulation = Simulation.query.filter(Simulation.id == simulation_id).first()
        if not simulation:
            raise SimulationNotFoundException
        if simulation.is_frozen:
            raise SimulationUsedException

        # Remove manually all child relations with quotes and funders
        # This is dirty, I admit it. :/
        for simulation_quote in simulation.simulation_quotes:
            SimulationQuoteService.delete_by_id(simulation_quote.id)
        for simulation_funder in simulation.simulation_funders:
            SimulationFunderService.delete_by_id(simulation_funder.id)
        for simulation_accommodation in simulation.simulations_accommodations:
            simulations_accommodations_service.SimulationAccommodationService.delete_by_id(
                simulation_accommodation.id
            )
        for sub_result in simulation.sub_results:
            sub_resuts_service.SimulationSubResultService.delete_by_id(sub_result.id)
        db.session.delete(simulation)
        db.session.commit()
        return simulation_id


class SimulationUseCaseService:
    @staticmethod
    def create(new_attrs: SimulationUseCaseInterface) -> SimulationUseCase:
        SimulationService.get_by_id(new_attrs.get("simulation_id"))
        use_case = SimulationUseCase(**new_attrs)
        db.session.add(use_case)
        db.session.commit()
        return use_case

    @staticmethod
    def create_list(
        use_cases_values: List[SimulationUseCaseInterface], simulation_id: int,
    ) -> List[SimulationUseCase]:

        use_cases = []
        # Create corresponding use cases
        for use_case in use_cases_values:
            use_case["simulation_id"] = simulation_id
            use_cases.append(SimulationUseCaseService.create(use_case))
        return use_cases

    @staticmethod
    def update_list(use_cases_fields, simulation_id):

        # Delete
        old_use_cases = SimulationUseCase.query.filter(
            SimulationUseCase.simulation_id == simulation_id
        ).all()
        for old_use_case in old_use_cases:
            SimulationUseCaseService.delete_by_id(old_use_case.id)

        use_cases = []
        # Re-create
        for wt in use_cases_fields:
            wt["simulation_id"] = simulation_id
            use_cases.append(SimulationUseCaseService.create(wt))

        # Remove all obsoletes relationships
        simulation = SimulationService.get_by_id(simulation_id)
        use_case_names = [use_case.use_case_name for use_case in simulation.use_cases]
        if "Dépôt" not in use_case_names:
            simulation_uses_service.SimulationDepositService.delete_all(simulation.id)
        if "Paiement" not in use_case_names:
            simulation_uses_service.SimulationPaymentRequestService.delete_all(
                simulation.id
            )
        if "Dossier agréé" not in use_case_names:
            simulation_uses_service.SimulationCertifiedService.delete_all(simulation.id)

        db.session.commit()
        return use_cases

    @staticmethod
    def delete_by_id(use_case_id: int) -> int or None:
        use_case = SimulationUseCase.query.filter(
            SimulationUseCase.id == use_case_id
        ).first()
        if not use_case:
            raise UseCaseSimulationNotFoundException
        db.session.delete(use_case)
        db.session.commit()
        return use_case_id


class SimulationQuoteService:
    @staticmethod
    def create(simulation_id: str, base_quote_id: str) -> SimulationQuote:
        simulation = SimulationService.get_by_id(simulation_id)
        if simulation.is_frozen:
            raise SimulationUsedException()
        base_quote = quotes_service.QuoteService.get_by_id(base_quote_id)
        if base_quote.id in [
            simulation_quote.base_quote_id
            for simulation_quote in simulation.simulation_quotes
        ]:
            # This quote is already linked to the simulation. The adding must be canceled
            return

        new_attrs = {
            "simulation_id": simulation_id,
            "base_quote_id": base_quote_id,
        }

        simulation_quote = SimulationQuote(**SimulationQuoteInterface(**new_attrs))
        db.session.add(simulation_quote)
        db.session.commit()
        return simulation_quote

    @staticmethod
    def update_list(
        simulation: SimulationInterface, quotes_values: List[QuoteInterface],
    ) -> List[SimulationQuote]:
        original_quotes_id = [
            simulation_quote.base_quote_id
            for simulation_quote in simulation.simulation_quotes
        ]
        changes_quotes_id = [
            quote_value["id"] for quote_value in quotes_values if "id" in quote_value
        ]
        # Create new quotes associations
        for change_id in changes_quotes_id:
            if change_id not in original_quotes_id:
                SimulationQuoteService.create(simulation.id, change_id)

        # Delete obsolete quotes associations
        for original_id in original_quotes_id:
            if original_id not in changes_quotes_id:
                SimulationQuoteService.delete_by_quotes_id(
                    {"quotes_id": [original_id]}, simulation.id
                )

        return simulation.simulation_quotes

    @staticmethod
    def create_by_quotes_id(quotes_id, simulation_id):
        simulation = SimulationService.get_by_id(simulation_id)
        for new_quote_id in quotes_id["quotes_id"]:
            SimulationQuoteService.create(simulation_id, new_quote_id)
        return simulation

    @staticmethod
    def delete_by_id(simulation_quote_id: int) -> int or None:
        simulation_quote = SimulationQuote.query.filter(
            SimulationQuote.id == simulation_quote_id
        ).first()
        if not simulation_quote:
            raise SimulationQuoteNotFoundException
        db.session.delete(simulation_quote)
        db.session.commit()
        return simulation_quote_id

    @staticmethod
    def delete_by_quotes_id(quotes_id, simulation_id):
        simulation = SimulationService.get_by_id(simulation_id)
        for removed_quote_id in quotes_id["quotes_id"]:
            for simulation_quote in simulation.simulation_quotes:
                if removed_quote_id == simulation_quote.base_quote.id:
                    SimulationQuoteService.delete_by_id(simulation_quote.id)
        return simulation


class SimulationFunderService:
    @staticmethod
    def create(
        simulation_id: str, new_attrs: SimulationFunderInterface
    ) -> SimulationFunder:
        """
        A simulation_funder join entity must contain a "base funder" AND a clone, because
        we need the funder data to be possibly overwritten"
        """
        simulation = SimulationService.get_by_id(simulation_id)
        if simulation.is_frozen:
            # A simulation cannot be modified if it's already used as "official deposit"
            raise SimulationUsedException()
        base_funder = funders_service.FunderService.get_by_id(new_attrs["funder"]["id"])
        if base_funder.is_duplicate:
            # A clone funder should not be cloned himself
            raise CloneFunderException()

        new_attrs["simulation_id"] = simulation_id
        new_attrs["base_funder_id"] = base_funder.id

        extracted_fields = ServicesUtils.clean_attrs(
            new_attrs, ["reset_scenario", "scenario", "funder", "funder_accommodations"]
        )

        simulation_funder = SimulationFunder(**SimulationFunderInterface(**new_attrs))
        # Create duplicate funder :
        duplicate_funder = funders_service.FunderService.duplicate(base_funder.id)
        simulation_funder.duplicate_funder = duplicate_funder

        db.session.add(simulation_funder)
        db.session.commit()

        # Set the adequate scenario for the parent project/requester situation
        quotes_id = [
            simulation_quote.base_quote_id
            for simulation_quote in simulation.simulation_quotes
        ]
        simulation_funder.match_scenario = funding_scenario_service.FundingScenarioService.get_match_scenarios(
            simulation_funder.duplicate_funder,
            simulation_funder.simulation.project_id,
            quotes_id=quotes_id,
        )

        if "funder_accommodations" in extracted_fields:
            funder_accommodations_service.FunderAccommodationService.create_update_list(
                extracted_fields.get("funder_accommodations"), simulation_funder.id
            )

        return simulation_funder

    @staticmethod
    def get_by_id(simulation_funder_id: str) -> SimulationFunder:
        db_simulation_funder = SimulationFunder.query.get(simulation_funder_id)
        if db_simulation_funder is None:
            raise SimulationFunderNotFoundException
        return db_simulation_funder

    @staticmethod
    def reset_funder(simulation_funder_id):
        """ Reset a funder linked to a simulation to his initial state.
        At the end of the operation, the "duplicate_funder" has the same values
        as the "base_funder" within a simulation_funder entity """
        simulation_funder = SimulationFunderService.get_by_id(simulation_funder_id)
        base_funder = simulation_funder.base_funder

        changes = base_funder.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(changes):
            if key not in base_funder.__table__.columns.keys():
                del changes[key]
        # Remove auto_generated values :
        del changes["id"]
        del changes["updated_at"]
        del changes["created_at"]
        # Update funder values
        duplicate_funder = funders_service.FunderService.update(
            simulation_funder.duplicate_funder, changes
        )

        # Reset funding scenarios (by deleting then re-duplicating them)
        for funding_scenario in duplicate_funder.funding_scenarios:
            funding_scenario_service.FundingScenarioService.delete_by_id(
                funding_scenario.id
            )
        for funding_scenario in base_funder.funding_scenarios:
            duplicate_funder.funding_scenarios.append(
                funding_scenario_service.FundingScenarioService.duplicate(
                    funding_scenario.id, duplicate_funder.id
                )
            )

        quotes_id = [
            simulation_quote.base_quote_id
            for simulation_quote in simulation_funder.simulation.simulation_quotes
        ]
        # Set the adequate scenario for the parent project/requester situation
        simulation_funder.match_scenario = funding_scenario_service.FundingScenarioService.get_match_scenarios(
            simulation_funder.duplicate_funder,
            simulation_funder.simulation.project_id,
            quotes_id=quotes_id,
        )
        db.session.commit()
        return simulation_funder

    @staticmethod
    def get_reinitialized_simulations_funders(
        project_id=None,
        funders_id=None,
        accommodations_id=None,
        quotes_id=None,
        requester_type="PO",
    ):
        if (
            not project_id
            or not funders_id
            or requester_type is not None
            and requester_type not in RequesterTypes.__members__
        ):
            raise InvalidParamsRequestException

        if accommodations_id is None:
            accommodations_id = []

        if not isinstance(funders_id, collections.Iterable):
            funders_id = [funders_id]
        funders_infos = []
        for funder_id in funders_id:
            funder = funders_service.FunderService.get_by_id(funder_id)
            if not funder.is_duplicate:
                base_funder = funder
            else:
                base_funder = (
                    SimulationFunder.query.filter(
                        SimulationFunder.duplicate_funder_id == funder.id
                    )
                    .first()
                    .base_funder
                )
            match_scenario = funding_scenario_service.FundingScenarioService.get_match_scenarios(
                base_funder, project_id, quotes_id=quotes_id
            )

            new_simulation_funder = {
                "funder": base_funder,
                "base_funder_id": base_funder.id,
                "scenario": match_scenario,
                "rate": None,
                "advance": None,
                "subventioned_expense": None,
                "reset_scenario": funder.is_duplicate,
                # We reset scenario only when front asked for a clone funder reset
            }
            if requester_type == RequesterTypes.PB.value:
                funder_accommodations = funder_accommodations_service.FunderAccommodationService.construct_initial_funder_accommodations(
                    base_funder,
                    project_id,
                    accommodations_id,
                    quotes_id,
                    match_scenario,
                )
                new_simulation_funder["funder_accommodations"] = funder_accommodations
            funders_infos.append(new_simulation_funder)
        return funders_infos

    @staticmethod
    def update(
        simulation_funder: SimulationFunder, changes: SimulationFunderInterface,
    ) -> Simulation:
        extracted_fields = ServicesUtils.clean_attrs(
            changes,
            [
                "funder",
                "scenario",
                "simulation_funder_id",
                "reset_scenario",
                "funder_accommodations",
            ],
        )
        reset_scenario = (
            "reset_scenario" in extracted_fields
            and extracted_fields["reset_scenario"] is True
        )
        simulation_funder.update(changes)
        db.session.commit()

        if "funder_accommodations" in extracted_fields:
            funder_accommodations_service.FunderAccommodationService.create_update_list(
                extracted_fields.get("funder_accommodations"),
                simulation_funder.id,
                reset_scenario=reset_scenario,
            )

        # Only when front/client specified a reset we effectively reset the funder
        if reset_scenario:
            SimulationFunderService.reset_funder(simulation_funder.id)

        return simulation_funder

    @staticmethod
    def update_list(
        simulation: Simulation, simulation_funders_values,
    ) -> List[SimulationFunder]:

        original_funders_id = [
            simulation_funder.id for simulation_funder in simulation.simulation_funders
        ]

        # Create or update funders/simulations associations
        for simulation_funder_value in simulation_funders_values:
            # New SimulationFunder must be created
            if "simulation_funder_id" not in simulation_funder_value:
                SimulationFunderService.create(
                    simulation.id, simulation_funder_value.copy()
                )
            # An existing SimulationFunder must be updated
            if "simulation_funder_id" in simulation_funder_value:
                simulation_funder = SimulationFunderService.get_by_id(
                    simulation_funder_value["simulation_funder_id"]
                )
                SimulationFunderService.update(
                    simulation_funder, simulation_funder_value.copy()
                )
        db.session.commit()

        # Delete obsolete associations
        change_simulation_funders_id = [
            simulation_funder["simulation_funder_id"]
            for simulation_funder in simulation_funders_values
            if "simulation_funder_id" in simulation_funder
        ]
        for original_id in original_funders_id:
            if original_id not in change_simulation_funders_id:
                SimulationFunderService.delete_by_id(original_id)

        return simulation.simulation_funders

    @staticmethod
    def create_by_funders_id(funders_id, simulation_id):
        """ Obsolete """
        simulation = SimulationService.get_by_id(simulation_id)
        for new_funder_id in funders_id["funders_id"]:
            SimulationFunderService.create(
                simulation_id, {"funder": {"id": new_funder_id}}
            )
        return simulation

    @staticmethod
    def delete_by_id(simulation_funder_id: int) -> int or None:
        simulation_funder = SimulationFunder.query.filter(
            SimulationFunder.id == simulation_funder_id
        ).first()
        if not simulation_funder:
            raise UseCaseSimulationNotFoundException

        # Delete children funder_accommodations, by setting them to []
        funder_accommodations_service.FunderAccommodationService.create_update_list(
            [], simulation_funder.id
        )
        # Delete child clone funder
        funders_service.FunderService.delete_by_id(
            simulation_funder.duplicate_funder.id
        )
        db.session.delete(simulation_funder)
        db.session.commit()
        return simulation_funder_id

    @staticmethod
    def delete_by_funders_id(funders_id, simulation_id):
        simulation = SimulationService.get_by_id(simulation_id)
        for removed_funder_id in funders_id["funders_id"]:
            for simulation_funder in simulation.simulation_funders:
                if removed_funder_id == simulation_funder.duplicate_funder.id:
                    SimulationFunderService.delete_by_id(simulation_funder.id)
        return simulation

    @staticmethod
    def has_changed(
        simulation_funder: SimulationFunder, changes: SimulationFunderInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(simulation_funder, key) != value:
                return True
        return False

    @staticmethod
    def duplicate_simulation_funders(
        source_simulation_id: int, new_simulation_id: int
    ) -> Simulation:
        """
        Duplicate all simulation_funders from a simulation to another
        """

        source_simulation = SimulationService.get_by_id(source_simulation_id)
        new_simulation = SimulationService.get_by_id(new_simulation_id)

        for simulations_funder in source_simulation.simulation_funders:
            args = {
                "funder": {"id": simulations_funder.base_funder_id},
                "rate": simulations_funder.rate,
                "advance": simulations_funder.advance,
                "subventioned_expense": simulations_funder.subventioned_expense,
            }
            new_simulation_funder = SimulationFunderService.create(
                new_simulation_id, args
            )
            funder_accommodations_service.FunderAccommodationService.duplicate_funders_accommodations(
                simulations_funder.id, new_simulation_funder.id
            )

        return new_simulation
