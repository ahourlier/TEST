from app import db
from app.common.address.service import AddressService
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.moe.interface import MoeInterface
from app.copro.moe.model import Moe


class MoeService:

    @staticmethod
    def create(new_attrs: MoeInterface) -> int:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        if new_attrs.get("address"):
            new_attrs["address_id"] = AddressService.create_address(new_attrs.get("address"))
            del new_attrs["address"]

        new_moe = Moe(**new_attrs)
        db.session.add(new_moe)
        db.session.commit()
        return new_moe.id

    @staticmethod
    def update(moe: Moe, changes: MoeInterface):
        if changes.get("phone_number", None):
            PhoneNumberService.update_phone_numbers(
                moe, [changes.get("phone_number")]
            )
            del changes["phone_number"]

        if changes.get("address"):
            if not moe.address_id:
                moe.address_id = AddressService.create_address(changes.get("address"))
            else:
                AddressService.update_address(moe.address_id, changes.get("address"))
            del changes["address"]

        moe.update(changes)
        db.session.commit()
        return moe
