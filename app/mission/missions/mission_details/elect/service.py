from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.mission.missions.mission_details.elect.exceptions import (
    ElectNotFoundException,
)
from app.mission.missions.mission_details.elect.model import Elect


class ElectService:
    @staticmethod
    def create(elect):
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
