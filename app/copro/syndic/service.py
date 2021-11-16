from flask_sqlalchemy import Pagination
from sqlalchemy import or_, and_

from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.app_name import App
from app.common.search import sort_query
from app.syndic.cadastre import Cadastre
from app.syndic.syndics.exceptions import (
    SyndicNotFoundException,
    MissionNotTypeSyndicException,
)
from app.syndic.syndics.interface import SyndicInterface
from app.syndic.syndics.model import Syndic
from app.syndic.syndic.interface import SyndicInterface
from app.mission.missions.service import MissionService


class SyndicService:

    @staticmethod
    def create(new_attrs: SyndicInterface) -> Syndic:
        pass


    @staticmethod
    def update(db_syndic: Syndic, changes: SyndicInterface, syndic_id: int) -> Syndic:

        if changes.get("cadastres"):
            delete_cadastres = Cadastre.__table__.delete().where(
                Cadastre.syndic_id == syndic_id
            )
            db.session.execute(delete_cadastres)
            db.session.commit()

            for c in changes.get("cadastres"):
                c["syndic_id"] = syndic_id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

            del changes["cadastres"]

        if changes.get("address_1"):
            if not db_syndic.address_1_id:
                changes["address_1_id"] = AddressService.create_address(
                    changes.get("address_1")
                )
            else:
                AddressService.update_address(
                    db_syndic.address_1_id, changes.get("address_1")
                )
            del changes["address_1"]

        if changes.get("address_2"):
            if not db_syndic.address_2_id:
                changes["address_2_id"] = AddressService.create_address(
                    changes.get("address_2")
                )
            else:
                AddressService.update_address(
                    db_syndic.address_1_id, changes.get("address_2")
                )
            del changes["address_2"]

        if changes.get("user_in_charge"):
            changes["user_in_charge_id"] = changes.get("user_in_charge").get("id")
            del changes["user_in_charge"]

        db_syndic.update(changes)
        db.session.commit()

        return db_syndic

    @staticmethod
    def delete(syndic_id: int):
        current_syndic = SyndicService.get(syndic_id)
        if current_syndic:
            current_syndic.soft_delete()
            db.session.commit()
        return syndic_id
