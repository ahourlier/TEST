import json

from app import db
from app.common.search import SearchService
from app.funder.funders import Funder
from app.funder.funders.error_handlers import FunderNotFoundException
from app.funder.funding_scenarios.error_handlers import (
    FundingScenarioNotFoundException,
    FundingScenarioFunderChangeException,
)
from app.funder.error_handlers import ValidationException
from app.funder.funding_scenarios.interface import FundingScenarioInterface
from app.common.exceptions import InconsistentUpdateIdException
from app.funder.funding_scenarios.model import (
    FundingScenario,
    FUNDING_SCENARIOS_CRITERIA_CONFIGURATION,
)
import app.funder.funders.service as funder_service
import app.project.projects.service as projects_service
import app.project.quotes.service as quotes_service
from app.project import Accommodation
from app.project.projects import Project


class FundingScenarioService:
    @staticmethod
    def get_all(funder_id=None):
        query = FundingScenario.query.order_by(FundingScenario.created_at)
        if funder_id:
            funder_service.FunderService.get_by_id(funder_id)
            query = query.filter(FundingScenario.funder_id == funder_id)

        return query.all()

    @staticmethod
    def get_by_id(funding_scenario_id: int) -> FundingScenario:
        db_funding_scenario = FundingScenario.query.get(funding_scenario_id)
        if db_funding_scenario is None:
            raise FundingScenarioNotFoundException
        return db_funding_scenario

    @staticmethod
    def create(
        new_attrs: FundingScenarioInterface, commit: bool = False
    ) -> FundingScenario:
        if "funder_id" not in new_attrs:
            raise FunderNotFoundException

        funder_service.FunderService.get_by_id(new_attrs["funder_id"])
        try:
            new_funding_scenario = FundingScenario(**new_attrs)
        except AssertionError as e:
            raise ValidationException(e.args[0])

        db.session.add(new_funding_scenario)
        if commit:
            db.session.commit()
        return new_funding_scenario

    @staticmethod
    def duplicate(funding_scenario_id: str, new_parent_id: str):
        base_fs = FundingScenarioService.get_by_id(funding_scenario_id)
        duplicate_dict = base_fs.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(duplicate_dict):
            if key not in base_fs.__table__.columns.keys():
                del duplicate_dict[key]
        # Remove auto_generated values :
        del duplicate_dict["id"]
        del duplicate_dict["updated_at"]
        del duplicate_dict["created_at"]
        # Replace parent funder id :
        duplicate_dict["funder_id"] = new_parent_id
        duplicate_fs = FundingScenarioService.create(
            FundingScenarioInterface(**duplicate_dict)
        )
        return duplicate_fs

    @staticmethod
    def update(
        funding_scenario: FundingScenario,
        changes: FundingScenarioInterface,
        force_update: bool = False,
        commit: bool = False,
    ) -> FundingScenario:
        if force_update or funder_service.FunderService.has_changed(
            funding_scenario, changes
        ):
            if changes.get("id") and changes.get("id") != funding_scenario.id:
                raise InconsistentUpdateIdException

            if changes.get("funder_id") and funding_scenario.funder_id != changes.get(
                "funder_id"
            ):
                raise FundingScenarioFunderChangeException

            try:
                funding_scenario.update(changes)
            except AssertionError as e:
                raise ValidationException(e.args[0])
            if commit:
                db.session.commit()
        return funding_scenario

    @staticmethod
    def has_changed(
        funding_scenario: FundingScenario, changes: FundingScenarioInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(funding_scenario, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(funding_scenario_id: int, commit: bool = False) -> int:
        db_funding_scenario = FundingScenario.query.get(funding_scenario_id)
        if not db_funding_scenario:
            raise FunderNotFoundException
        db.session.delete(db_funding_scenario)
        if commit:
            db.session.commit()
        return funding_scenario_id

    @staticmethod
    def get_match_scenarios(
        funder: Funder, project_id: str, accommodation_id: str = None, quotes_id=[]
    ) -> FundingScenario:
        match_scenario = None
        for scenario in funder.funding_scenarios:
            if FundingScenarioService.check_scenario_compliance(
                scenario,
                project_id,
                quotes_id=quotes_id,
                accommodation_id=accommodation_id,
            ):
                if match_scenario:
                    # Error case : another scenario already matches.
                    return None
                match_scenario = scenario

        return match_scenario

    @staticmethod
    def check_scenario_compliance(
        funding_scenario, project_id, quotes_id=[], accommodation_id: str = None,
    ) -> bool:
        # Return true if the provided project (and the optional accommodation) fit all scenario criterium
        requester_type = projects_service.ProjectService.get_by_id(
            project_id
        ).requester.type
        formatted_criteria = FundingScenarioService.format_criteria(
            funding_scenario.criteria
        )
        (
            project_criteria,
            accommodation_criteria,
            work_types_criteria,
        ) = FundingScenarioService.apply_business_rules_to_criteria(
            formatted_criteria, project_id, accommodation_id, requester_type
        )
        work_types_criteria_match = FundingScenarioService.check_work_type_matching(
            work_types_criteria, quotes_id=quotes_id, accommodation_id=accommodation_id
        )
        # We verify if one specific project matches the scenario
        match_project = SearchService.search_into_model(
            Project, {"filters": project_criteria}
        ).first()

        # If an accommodation_id have been provided =>
        # we also verify it matches the scenario
        if accommodation_id is not None:
            match_accommodation = SearchService.search_into_model(
                Accommodation, {"filters": accommodation_criteria}
            ).first()
            return (
                match_project is not None
                and match_accommodation is not None
                and work_types_criteria_match
            )
        return match_project is not None and work_types_criteria_match

    @staticmethod
    def format_criteria(criteria) -> dict:
        """ We shall use the search module to look for appropriate funding_scenario.
        So we must parse the criteria into to a search compliant format"""
        local_criteria = json.loads(json.dumps(criteria))
        OPERATORS_CONVERTION = {
            "<": "lt",
            "<=": "lte",
            "=": "eq",
            ">=": "gte",
            ">": "gt",
            "in": "in",
        }

        for criterion in local_criteria:
            criterion["op"] = criterion.pop("operator")
            criterion["values"] = criterion.pop("value")
            criterion_configuration = FUNDING_SCENARIOS_CRITERIA_CONFIGURATION[
                criterion["field"]
            ]
            if "operators_overrides" in criterion_configuration:
                criterion["op"] = OPERATORS_CONVERTION[
                    criterion_configuration["operators_overrides"][criterion["op"]]
                ]
            else:
                criterion["op"] = OPERATORS_CONVERTION[criterion["op"]]
            criterion["values"] = [criterion["values"]]

        return local_criteria

    @staticmethod
    def apply_business_rules_to_criteria(
        criteria, project_id, accommodation_id, requester_type
    ):
        """
        Each criteria has his "own business rule", depending on requester type ("PB" or "PO") and on the necessity (or not)
        to sort criteria by a specific accommodation
        """
        FIELDS_TO_REMOVE_IN_PB = [
            "accommodations.purchase_year",
            "requester.resources_category",
            "requester.profession",
        ]

        accommodation_criteria = []
        project_criteria = []
        work_type_criteria = []

        for criterion in criteria:

            if (
                accommodation_id is not None
                and criterion["field"] == "accommodations.vacant"
            ):
                # If accomodation_id have been provided,
                # the "vacant" criteria must be extracted to be injected in a specific "Accommodation search"
                criterion["field"] = "vacant"
                accommodation_criteria.append(criterion)
                continue

            if accommodation_id is not None and criterion["field"] == "type":
                # If accommodation_id have been provided,
                # the "type" criteria must be extracted to be injected in a specific "Accommodation search"
                criterion["field"] = "case_type"
                accommodation_criteria.append(criterion)
                continue

            if (
                accommodation_id is not None
                and criterion["field"] == "secondary_case_type"
            ):
                # If accommodation_id have been provided,
                # the "secondary_case_type" criteria must be extracted to be injected in a specific "Accommodation search"
                criterion["field"] = "secondary_case_type"
                accommodation_criteria.append(criterion)
                continue
            
            if (
                accommodation_id is not None
                and criterion["field"] == "accommodations.type_rent_after_renovation"
            ):
                # If accommodation_id have been provided,
                # the "type_rent_after_renovation" criteria must be extracted to be injected in a specific "Accommodation search"
                criterion["field"] = "type_rent_after_renovation"
                accommodation_criteria.append(criterion)
                continue

            # Business rule : if project address is empty, we must search on requester address instead
            if criterion["field"] == "address_location":
                project = projects_service.ProjectService.get_by_id(project_id)
                if project.address_location is None:
                    criterion["field"] = "requester.address_location"

            if requester_type == "PB":
                # Business rule : on PB search, scenario purchase_year must match on common_area table.
                if criterion["field"] == "accommodations.purchase_year":
                    criterion["field"] = "common_areas.purchase_year"
                if criterion["field"] in FIELDS_TO_REMOVE_IN_PB:
                    continue

            if criterion["field"] == "work_types.type_name":
                # We extract work types because they functionaly must be passed on a specific matching workflow
                work_type_criteria.append(criterion)
                continue

            project_criteria.append(criterion)

        project_criteria.append({"field": "id", "op": "eq", "values": [project_id]})
        accommodation_criteria.append(
            {"field": "id", "op": "eq", "values": [accommodation_id]}
        )

        return project_criteria, accommodation_criteria, work_type_criteria

    @staticmethod
    def check_work_type_matching(
        work_types_criterium, quotes_id=[], accommodation_id=None
    ):
        """ Return True if all work_types_criterium "values" are in quotes 's work_types, else False.
        If an accommodation_id is provided, remove all quotes that does not contain the linked accommodation"""
        if not work_types_criterium or len(work_types_criterium) == 0:
            # No work types was present into scenario criterium, so work_type_matching is True by default
            return True
        if not quotes_id:
            return False
        quotes_work_types_to_check = []
        for quote_id in quotes_id:
            quote = quotes_service.QuoteService.get_by_id(quote_id)
            if accommodation_id and accommodation_id not in [
                quotes_accommodation.accommodation_id
                for quotes_accommodation in quote.quotes_accommodations
            ]:
                continue  # Skip this quote because it does not contain the provided accommodation
            quote_work_types = [work_type.type_name for work_type in quote.work_types]
            quotes_work_types_to_check.extend(quote_work_types)
        # Final matching verification
        for criterium in work_types_criterium:
            for value in criterium["values"]:
                if value not in quotes_work_types_to_check:
                    return False
        return True
