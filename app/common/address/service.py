from app import db
from app.common.address.model import Address


class AddressService:
    @staticmethod
    def create_address(address):
        new_address = Address(**address)
        db.session.add(new_address)
        db.session.commit()
        return new_address.id

    @staticmethod
    def update_address(address_id, address):
        if address is None:
            Address.query.filter(Address.id == address_id).delete()
            return
        db_address = Address.query.get(address_id)
        if not db_address:
            return
        db_address.update(address)
        db.session.commit()
        return
