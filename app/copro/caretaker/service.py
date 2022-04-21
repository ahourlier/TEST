from app import db
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.caretaker.interface import CareTakerInterface
from app.copro.caretaker.model import CareTaker


class CareTakerService:
    @staticmethod
    def create(new_attrs: CareTakerInterface) -> int:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        new_caretaker = CareTaker(**new_attrs)
        db.session.add(new_caretaker)
        db.session.commit()
        return new_caretaker.id

    @staticmethod
    def update(caretaker: CareTaker, changes: CareTakerInterface):

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    caretaker, [changes.get("phone_number")]
                )
            else:
                if len(caretaker.phones) > 0:
                    PhoneNumber.query.filter(
                        PhoneNumber.id == caretaker.phones[0].id
                    ).delete()
                    db.session.commit()
            del changes["phone_number"]

        caretaker.update(changes)
        db.session.commit()
        return caretaker
