from app import db
from app.common.address.model import Address


class AddressService:

    @staticmethod
    def create_address(address):
        new_address = Address(**address)
        db.session.add(new_address)
        db.session.commit()
        return new_address.id
