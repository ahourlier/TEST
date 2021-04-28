from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from .error_handlers import AgencyNotFoundException, AgencyDuplicateNameException
from .exceptions import ChildAntennaException, ChildAgencyMissionException
from .interface import AgencyInterface
from .model import Agency
from app import db
from app.admin.error_handlers import InconsistentUpdateIdException
from ...common.search import sort_query
import app.admin.antennas.service as antenna_service
from ...mission.missions.model import MissionStatus

AGENCIES_DEFAULT_PAGE = 1
AGENCIES_DEFAULT_PAGE_SIZE = 100
AGENCIES_DEFAULT_SORT_FIELD = "id"
AGENCIES_DEFAULT_SORT_DIRECTION = "desc"


class AgencyService:
    @staticmethod
    def get_all(
        page=AGENCIES_DEFAULT_PAGE,
        size=AGENCIES_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=AGENCIES_DEFAULT_SORT_FIELD,
        direction=AGENCIES_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        q = sort_query(Agency.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Agency.name.ilike(search_term),
                    Agency.postal_address.ilike(search_term),
                )
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(agency_id: str) -> Agency:
        db_agency = Agency.query.get(agency_id)
        if db_agency is None:
            raise AgencyNotFoundException
        return db_agency

    @staticmethod
    def create(new_attrs: AgencyInterface) -> Agency:
        new_agency = Agency(**new_attrs)
        existing_agency = Agency.query.filter(
            Agency.name.ilike(new_attrs.get("name"))
        ).first()
        if existing_agency is not None:
            raise AgencyDuplicateNameException
        db.session.add(new_agency)
        db.session.commit()
        # Each agency is created by default with an antenna,
        # with has the same fields attributes than his parent.
        new_antenna_fields = {
            "name": new_agency.name,
            "postal_address": new_agency.postal_address,
            "email_address": new_agency.email_address,
            "agency_id": new_agency.id,
        }
        antenna_service.AntennaService.create(new_antenna_fields)

        return new_agency

    @staticmethod
    def update(
        agency: Agency, changes: AgencyInterface, force_update: bool = False
    ) -> Agency:
        if force_update or AgencyService.has_changed(agency, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != agency.id:
                raise InconsistentUpdateIdException()
            if changes.get("name") != agency.name:
                existing_agency = Agency.query.filter(
                    Agency.name.ilike(changes.get("name"))
                ).first()
                if existing_agency and existing_agency.id != agency.id:
                    raise AgencyDuplicateNameException
            agency.update(changes)
            db.session.commit()
        return agency

    @staticmethod
    def has_changed(agency: Agency, changes: AgencyInterface) -> bool:
        for key, value in changes.items():
            if getattr(agency, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(agency_id: int) -> int or None:
        agency = Agency.query.filter(Agency.id == agency_id).first()
        if not agency:
            raise AgencyNotFoundException
        if agency.antennas:
            raise ChildAntennaException
        if agency.missions:
            for mission in agency.missions:
                if mission.status != MissionStatus.ARCHIVED and not mission.is_deleted:
                    raise ChildAgencyMissionException()

        db.session.delete(agency)
        db.session.commit()
        return agency_id
