from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.antennas.error_handlers import (
    AntennaNotFoundException,
    AntennaDuplicateNameException,
)
from app.admin.antennas.exceptions import ChildAntennaMissionException
from app.admin.error_handlers import InconsistentUpdateIdException
import app.admin.agencies.service as agency_service
from app.admin.antennas import Antenna
from app.admin.antennas.interface import AntennaInterface
from app.common.exceptions import ChildMissionException
from app.common.search import sort_query

from app import db
from app.mission.missions.model import MissionStatus

ANTENNAS_DEFAULT_PAGE = 1
ANTENNAS_DEFAULT_PAGE_SIZE = 100
ANTENNAS_DEFAULT_SORT_FIELD = "id"
ANTENNAS_DEFAULT_SORT_DIRECTION = "desc"


class AntennaService:
    @staticmethod
    def get_all(
        page=ANTENNAS_DEFAULT_PAGE,
        size=ANTENNAS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
        direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
        agency_id=None,
    ) -> Pagination:
        q = sort_query(Antenna.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Antenna.name.ilike(search_term),
                    Antenna.postal_address.ilike(search_term),
                )
            )

        if agency_id is not None:
            q = q.filter(Antenna.agency_id == agency_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(antenna_id: str) -> Antenna:
        db_antenna = Antenna.query.get(antenna_id)
        if db_antenna is None:
            raise AntennaNotFoundException
        return db_antenna

    @staticmethod
    def create(new_attrs: AntennaInterface) -> Antenna:
        """Create a new antenna in a given agency"""
        try:
            agency_service.AgencyService.get_by_id(new_attrs.get("agency_id"))
        except AgencyNotFoundException as e:
            raise e
        else:
            existing_antenna = Antenna.query.filter(
                Antenna.name.ilike(new_attrs.get("name"))
            ).first()
            if existing_antenna is not None:
                raise AntennaDuplicateNameException
            antenna = Antenna(**new_attrs)
            db.session.add(antenna)
            db.session.commit()
            return antenna

    @staticmethod
    def update(
        antenna: Antenna, changes: AntennaInterface, force_update: bool = False
    ) -> Antenna:
        if force_update or AntennaService.has_changed(antenna, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != antenna.id:
                raise InconsistentUpdateIdException()
            if changes.get("name") != antenna.name:
                existing_antenna = Antenna.query.filter(
                    Antenna.name.ilike(changes.get("name"))
                ).first()
                if existing_antenna and existing_antenna.id != antenna.id:
                    raise AntennaDuplicateNameException
            antenna.update(changes)
            db.session.commit()
        return antenna

    @staticmethod
    def has_changed(antenna: Antenna, changes: AntennaInterface) -> bool:
        for key, value in changes.items():
            if getattr(antenna, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(antenna_id: int) -> int or None:
        antenna = Antenna.query.filter(Antenna.id == antenna_id).first()
        if not antenna:
            raise AntennaNotFoundException
        if antenna.missions:
            for mission in antenna.missions:
                if mission.status != MissionStatus.ARCHIVED and not mission.is_deleted:
                    raise ChildAntennaMissionException()
        db.session.delete(antenna)
        db.session.commit()
        return antenna_id
