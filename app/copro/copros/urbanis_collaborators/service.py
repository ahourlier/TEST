from app import db
from app.copro.copros.urbanis_collaborators.interface import (
    UrbanisCollaboratorsInterface,
)
from app.copro.copros.model import Copro
from app.auth.users.model import User
from app.copro.copros.model import UrbanisCollaborators


class UrbanisCollaboratorsService:
    def get(user_in_charge_id: int) -> UrbanisCollaborators:
        return UrbanisCollaborators.query.filter(
            user_in_charge_id == UrbanisCollaborators.user_in_charge_id
        ).all()

    def get_all(copro_id: int) -> UrbanisCollaborators:
        return UrbanisCollaborators.query.filter(
            copro_id == UrbanisCollaborators.copro_id
        ).all()

    @staticmethod
    def update(db_collab, changes: UrbanisCollaboratorsInterface):
        db_collab.update(changes)
        db.session.commit()
        return db_collab

    @staticmethod
    def add(item: UrbanisCollaboratorsInterface):
        obj = UrbanisCollaborators(**item)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete_by_copro_id(copro_id: int):
        UrbanisCollaborators.query.filter(
            copro_id == UrbanisCollaborators.copro_id
        ).delete()

        db.session.commit()

    @staticmethod
    def delete_by_user_in_charge_id(user_in_charge_id: int):
        UrbanisCollaborators.query.filter(
            user_in_charge_id == UrbanisCollaborators.user_in_charge_id
        ).delete()

        db.session.commit()
