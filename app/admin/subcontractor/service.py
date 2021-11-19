from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.search import sort_query
from app.mission.missions.mission_details.service import MissionDetailService
from app.admin.subcontractor import (
    Subcontractor,
    MissionDetailSubcontractor,
)
from app.admin.subcontractor.exceptions import SubcontractorNotFoundException

SUBCONTRACTORS_DEFAULT_PAGE = 1
SUBCONTRACTORS_DEFAULT_PAGE_SIZE = 100
SUBCONTRACTORS_DEFAULT_SORT_FIELD = "id"
SUBCONTRACTORS_DEFAULT_SORT_DIRECTION = "desc"


class SubcontractorService:
    @staticmethod
    def list(
        page=SUBCONTRACTORS_DEFAULT_PAGE,
        size=SUBCONTRACTORS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=SUBCONTRACTORS_DEFAULT_SORT_FIELD,
        direction=SUBCONTRACTORS_DEFAULT_SORT_DIRECTION,
    ) -> Pagination:
        q = sort_query(Subcontractor.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.join(Address).filter(
                or_(
                    Subcontractor.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        # Deactivated clients must not be retrieved
        q = q.filter(Subcontractor.active == True)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get(subcontractor_id) -> Subcontractor:
        sub = Subcontractor.query.get(subcontractor_id)
        if not sub:
            raise SubcontractorNotFoundException

        return sub

    @staticmethod
    def update(db_subcontractor: Subcontractor, new_attrs):

        if "address" in new_attrs:
            if new_attrs.get("address") is not None:
                if not db_subcontractor.address_id:
                    db_subcontractor.address_id = AddressService.create_address(
                        new_attrs.get("address")
                    )
                else:
                    db_address = Address.query.get(db_subcontractor.address_id)
                    db_address.update(new_attrs.get("address"))
            else:
                address = Address.query.filter(
                    Address.id == db_subcontractor.address_id
                )
                db_subcontractor.address_id = None
                address.delete()
            del new_attrs["address"]

        db_subcontractor.update(new_attrs)
        db.session.commit()
        return db_subcontractor

    @staticmethod
    def create(subcontractor):
        address_id = None
        if "address" in subcontractor and subcontractor.get("address") is not None:
            address_id = AddressService.create_address(subcontractor.get("address"))
            del subcontractor["address"]

        new_subcontractor = Subcontractor(**subcontractor)
        if address_id:
            new_subcontractor.address_id = address_id
        db.session.add(new_subcontractor)
        db.session.commit()

        return new_subcontractor

    @staticmethod
    def delete(subcontractor_id):

        subcontractor = Subcontractor.query.filter(
            Subcontractor.id == subcontractor_id
        ).first()

        if not subcontractor:
            raise SubcontractorNotFoundException

        q = db.session.query(MissionDetailSubcontractor).filter(
            MissionDetailSubcontractor.c.subcontractor_id == subcontractor_id
        )
        q.delete(synchronize_session=False)
        db.session.commit()

        # if subcontractor.address_id:
        #     address = Address.query.filter(Address.id == subcontractor.address_id)
        #     subcontractor.address_id = None
        #     address.delete()

        subcontractor.active = False

        # db.session.delete(subcontractor)
        db.session.commit()
        return subcontractor_id

    @staticmethod
    def link(mission_id, subcontractor_id):
        subcontractor = SubcontractorService.get(subcontractor_id)
        mission_details = MissionDetailService.get_by_mission_id(mission_id)
        subcontractor.mission_detail.append(mission_details)
        db.session.commit()
        return

    @staticmethod
    def unlink(mission_id, subcontractor_id):
        mission_details = MissionDetailService.get_by_mission_id(mission_id)
        q = (
            db.session.query(MissionDetailSubcontractor)
            .filter(MissionDetailSubcontractor.c.subcontractor_id == subcontractor_id)
            .filter(
                MissionDetailSubcontractor.c.mission_detail_id == mission_details.id
            )
        )
        q.delete(synchronize_session=False)
        db.session.commit()
        return
