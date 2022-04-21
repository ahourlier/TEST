from app import db
from app.common.address.service import AddressService
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.architect.interface import ArchitectInterface
from app.copro.architect.model import Architect


class ArchitectService:
    @staticmethod
    def create(new_attrs: ArchitectInterface) -> int:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        if new_attrs.get("address"):
            new_attrs["address_id"] = AddressService.create_address(
                new_attrs.get("address")
            )
            del new_attrs["address"]

        new_architect = Architect(**new_attrs)
        db.session.add(new_architect)
        db.session.commit()
        return new_architect.id

    @staticmethod
    def update(architect: Architect, changes: ArchitectInterface):

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    architect, [changes.get("phone_number")]
                )
            else:
                if len(architect.phones) > 0:
                    PhoneNumber.query.filter(
                        PhoneNumber.id == architect.phones[0].id
                    ).delete()
                    db.session.commit()
            del changes["phone_number"]

        if "address" in changes:
            if architect.address_id:
                if not changes.get("address"):
                    architect.address_id = None
                    changes["address_id"] = None
                AddressService.update_address(architect.address_id, changes.get("address"))
            else:
                if changes.get("address"):
                    changes["address_id"] = AddressService.create_address(
                        changes.get("address")
                    )
            del changes["address"]

        architect.update(changes)
        db.session.commit()
        return architect
