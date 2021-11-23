from app import db
from app.common.address.service import AddressService
from app.copro.syndic.exceptions import (
    SyndicNotFoundException,
    WrongSyndicTypeException,
)
from app.copro.syndic.model import Syndic
from app.copro.syndic.interface import SyndicInterface
from app.referential.enums.service import AppEnumService

SYNDIC_TYPE_ENUM = "SyndicType"
ENUMS = [SYNDIC_TYPE_ENUM]


class SyndicService:
    @staticmethod
    def get(syndic_id):
        syndic = Syndic.query.get(syndic_id)
        if not syndic:
            raise SyndicNotFoundException
        return syndic

    @staticmethod
    def create(new_attrs: SyndicInterface) -> Syndic:

        SyndicService.check_enums(new_attrs)
        if new_attrs.get("manager_address"):
            new_attrs["manager_address_id"] = AddressService.create_address(
                new_attrs.get("manager_address")
            )
            del new_attrs["manager_address"]

        new_syndic = Syndic(**new_attrs)
        db.session.add(new_syndic)
        db.session.commit()

        return new_syndic

    @staticmethod
    def update(db_syndic: Syndic, changes: SyndicInterface, syndic_id: int) -> Syndic:

        SyndicService.check_enums(changes)

        if "manager_address" in changes:
            if db_syndic.manager_address_id:
                if not changes.get("manager_address"):
                    db_syndic.manager_address_id = None
                    changes["manager_address_id"] = None
                AddressService.update_address(
                    db_syndic.manager_address_id, changes.get("manager_address")
                )
            else:
                if changes.get("manager_address"):
                    changes["manager_address_id"] = AddressService.create_address(
                        changes.get("manager_address")
                    )
            del changes["address"]

        db_syndic.update(changes)
        db.session.commit()
        return db_syndic

    @staticmethod
    def delete(syndic_id: int):
        current_syndic = SyndicService.get(syndic_id)
        Syndic.query.filter(Syndic.id == syndic_id).delete()
        db.session.commit()
        return syndic_id

    @staticmethod
    def check_enums(payload: SyndicInterface):
        enums = AppEnumService.get_enums(ENUMS)
        if payload.get("type") is not None and payload.get("type") not in enums.get(
            SYNDIC_TYPE_ENUM
        ):
            raise WrongSyndicTypeException

        return
