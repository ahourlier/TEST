from sqlalchemy import and_

from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.mission.missions.mission_details.model import MissionDetail
from app.mission.missions.mission_details.service import MissionDetailService
from app.mission.missions.mission_details.subcontractor import (
    Subcontractor,
    MissionDetailSubcontractor,
)
from app.mission.missions.mission_details.subcontractor.exceptions import (
    SubcontractorNotFoundException,
)


class SubcontractorService:
    @staticmethod
    def list():
        return Subcontractor.query.all()

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

        if subcontractor.address_id:
            address = Address.query.filter(Address.id == subcontractor.address_id)
            subcontractor.address_id = None
            address.delete()

        db.session.delete(subcontractor)
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
