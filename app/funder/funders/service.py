from operator import or_
from typing import List

from app import db
from app.funder.funders import Funder
from app.funder.funders.error_handlers import (
    FunderNotFoundException,
    FunderMissionChangeException,
)
from app.funder.funders.exceptions import FunderUsedBySimulationException
from app.funder.funders.interface import FunderInterface
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidSearchFieldException,
)
from app.common.search import sort_query
from app.funder.funding_scenarios import FundingScenario
import app.funder.funding_scenarios.service as funding_scenario_service
from app.mission.missions.service import MissionService
from app.project.requesters.model import RequesterTypes

FUNDERS_DEFAULT_PAGE = 1
FUNDERS_DEFAULT_PAGE_SIZE = 100
FUNDERS_DEFAULT_SORT_FIELD = "priority"
FUNDERS_DEFAULT_SORT_DIRECTION = "asc"


class FunderService:
    @staticmethod
    def get_all(
        page=FUNDERS_DEFAULT_PAGE,
        size=FUNDERS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=FUNDERS_DEFAULT_SORT_FIELD,
        direction=FUNDERS_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        requester_type=None,
    ):
        q = sort_query(Funder.query, sort_by, direction)
        q = q.filter(or_(Funder.is_deleted == False, Funder.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(Funder.name.ilike(search_term))

        # Filter by mission
        if mission_id is not None:
            q = q.filter(Funder.mission_id == mission_id)
        else:
            q = q.filter(Funder.is_national.is_(True))

        # Filter by requester_type
        if requester_type is not None and requester_type not in RequesterTypes.__members__:
            raise InvalidSearchFieldException()
        if requester_type is not None:
            q = q.filter(Funder.requester_type == requester_type)

        # Only orignal funders (and no clones) should be retrieved
        q = q.filter(Funder.is_duplicate == False)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(funder_id: int) -> Funder:
        db_funder = Funder.query.get(funder_id)
        if db_funder is None or db_funder.is_deleted:
            raise FunderNotFoundException
        return db_funder

    @staticmethod
    def create(new_attrs: FunderInterface, commit: bool = False) -> Funder:
        if new_attrs.get("mission_id") is not None:
            # will raise an exception if the mission does not exist
            MissionService.get_by_id(new_attrs.get("mission_id"))

        new_funder = Funder(**new_attrs)
        db.session.add(new_funder)
        if commit:
            db.session.commit()
        return new_funder

    @staticmethod
    def duplicate(funder_id: str):
        base_funder = FunderService.get_by_id(funder_id)
        duplicate_dict = base_funder.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(duplicate_dict):
            if key not in base_funder.__table__.columns.keys():
                del duplicate_dict[key]
        # Remove auto_generated values :
        del duplicate_dict["id"]
        del duplicate_dict["updated_at"]
        del duplicate_dict["created_at"]
        # Create new funder
        duplicated_funder = FunderService.create(FunderInterface(**duplicate_dict))
        # Duplicate funding scenarios
        for funding_scenario in base_funder.funding_scenarios:
            duplicated_funder.funding_scenarios.append(
                funding_scenario_service.FundingScenarioService.duplicate(
                    funding_scenario.id, duplicated_funder.id
                )
            )
        return duplicated_funder

    @staticmethod
    def update(
        funder: Funder,
        changes: FunderInterface,
        force_update: bool = False,
        commit: bool = False,
    ) -> Funder:
        if force_update or FunderService.has_changed(funder, changes):
            if changes.get("id") and changes.get("id") != funder.id:
                raise InconsistentUpdateIdException

            if changes.get("mission_id") and funder.mission_id != changes.get(
                "mission_id"
            ):
                raise FunderMissionChangeException
            if "funding_scenarios" in changes:
                del changes["funding_scenarios"]
            funder.update(changes)
            if commit:
                db.session.commit()
        return funder

    @staticmethod
    def has_changed(funder: Funder, changes: FunderInterface) -> bool:
        for key, value in changes.items():
            if getattr(funder, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(funder_id: int, commit: bool = False) -> int:
        db_funder = Funder.query.get(funder_id)
        if not db_funder:
            raise FunderNotFoundException
        db_funder.soft_delete()
        if commit:
            db.session.commit()
        return funder_id

    @staticmethod
    def copy_to_mission(
        funder: Funder, mission_id: int, commit: bool = False
    ) -> Funder:
        MissionService.get_by_id(mission_id)
        existing_scenarios = funding_scenario_service.FundingScenarioService.get_all(
            funder.id
        )
        new_scenarios = [
            FundingScenario(
                criteria=s.criteria,
                rate=s.rate,
                upper_limit=s.upper_limit,
                advance=s.advance,
                upper_surface_limit=s.upper_surface_limit,
                upper_price_surface_limit=s.upper_price_surface_limit,
            )
            for s in existing_scenarios
        ]
        new_funder = Funder(
            name=funder.name,
            subvention_round=funder.subvention_round,
            type=funder.type,
            priority=funder.priority,
            mission_id=mission_id,
            requester_type=funder.requester_type,
            funding_scenarios=new_scenarios,
        )

        db.session.add(new_funder)
        if commit:
            db.session.commit()
        return new_funder

    @staticmethod
    def copy_multiple_to_mission(mission_id: int, funders_id: List = []):
        funders = []
        for funder_id in funders_id:
            original_funder = FunderService.get_by_id(funder_id)
            funders.append(FunderService.copy_to_mission(original_funder, mission_id))
        db.session.commit()
        return funders
