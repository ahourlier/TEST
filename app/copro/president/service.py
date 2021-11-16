from app import db
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.president.interface import PresidentInterface
from app.copro.president.model import President


class PresidentService:

    @staticmethod
    def create(president: PresidentInterface):
        if "phone_number" in president:
            if president.get("phone_number", None):
                president["phones"] = [PhoneNumber(**president.get("phone_number"))]
            del president["phone_number"]
        new_president = President(**president)
        db.session.add(new_president)
        db.session.commit()
        return new_president.id

    @staticmethod
    def update(db_president, changes: PresidentInterface):
        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    db_president, [changes.get("phone_number")]
                )
            del changes["phone_number"]
        db_president.update(changes)
        db.session.commit()
        return db_president
