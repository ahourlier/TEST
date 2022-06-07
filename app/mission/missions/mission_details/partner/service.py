from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.mission.missions.mission_details.partner.error_handlers import (
    PartnerNotFoundException,
)
from app.mission.missions.mission_details.partner.model import Partner


class PartnerService:
    @staticmethod
    def create(partner):
        address = None
        if "address" in partner and partner.get("address") is not None:
            address = partner.get("address")
            del partner["address"]

        address_id = None
        if address:
            address_id = AddressService.create_address(address)

        new_partner = Partner(**partner)
        if address_id:
            new_partner.address_id = address_id
        db.session.add(new_partner)
        db.session.commit()

        return new_partner

    @staticmethod
    def get_by_id(partner_id: int):
        partner = Partner.query.get(partner_id)
        if not partner:
            raise PartnerNotFoundException
        return partner

    @staticmethod
    def update(db_partner: Partner, new_attrs):

        if "address" in new_attrs:
            if new_attrs.get("address") is not None:
                if not db_partner.address_id:
                    db_partner.address_id = AddressService.create_address(
                        new_attrs.get("address")
                    )
                else:
                    db_address = Address.query.get(db_partner.address_id)
                    db_address.update(new_attrs.get("address"))
            else:
                address = Address.query.filter(Address.id == db_partner.address_id)
                db_partner.address_id = None
                address.delete()
            del new_attrs["address"]

        db_partner.update(new_attrs)
        db.session.commit()
        return db_partner

    @staticmethod
    def delete(partner_id):
        partner = Partner.query.filter(Partner.id == partner_id).first()

        if not partner:
            raise PartnerNotFoundException

        if partner.address_id:
            address = Address.query.filter(Address.id == partner.address_id)
            partner.address_id = None
            address.delete()

        db.session.delete(partner)
        db.session.commit()
        return partner_id
