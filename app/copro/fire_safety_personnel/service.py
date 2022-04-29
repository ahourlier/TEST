from app import db
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.fire_safety_personnel.interface import FireSafetyPersonnelInterface
from app.copro.fire_safety_personnel.model import FireSafetyPersonnel


class FireSafetyPersonnelService:
    @staticmethod
    def create(new_attrs: FireSafetyPersonnelInterface) -> int:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        new_fire_safety_personnel = FireSafetyPersonnel(**new_attrs)
        db.session.add(new_fire_safety_personnel)
        db.session.commit()
        return new_fire_safety_personnel.id

    @staticmethod
    def update(
        fire_safety_personnel: FireSafetyPersonnel,
        changes: FireSafetyPersonnelInterface,
    ):

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    fire_safety_personnel, [changes.get("phone_number")]
                )
            else:
                if len(fire_safety_personnel.phones) > 0:
                    PhoneNumber.query.filter(
                        PhoneNumber.id == fire_safety_personnel.phones[0].id
                    ).delete()
                    db.session.commit()
            del changes["phone_number"]

        fire_safety_personnel.update(changes)
        db.session.commit()
        return fire_safety_personnel
