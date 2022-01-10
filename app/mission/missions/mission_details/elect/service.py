from app import db

from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.mission.missions.mission_details.elect.error_handlers import ElectNotFoundException
from app.mission.missions.mission_details.elect.model import Elect


class ElectService:
    @staticmethod
    def create(elect):
        if "phone_number" in elect:
            if elect.get("phone_number", None):
                elect["phones"] = [PhoneNumber(**elect.get("phone_number"))]
            del elect["phone_number"]
        new_elect = Elect(**elect)
        db.session.add(new_elect)
        db.session.commit()

        return new_elect

    @staticmethod
    def get_by_id(elect_id: int):
        elect = Elect.query.get(elect_id)
        if not elect:
            raise ElectNotFoundException
        return elect

    @staticmethod
    def update(db_elect: Elect, new_attrs):
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    db_elect, [new_attrs.get("phone_number")]
                )
            del new_attrs["phone_number"]
        db_elect.update(new_attrs)
        db.session.commit()
        return db_elect

    @staticmethod
    def delete(elect_id):
        elect = Elect.query.filter(Elect.id == elect_id).first()

        if not elect:
            raise ElectNotFoundException

        db.session.delete(elect)
        db.session.commit()
        return elect_id
