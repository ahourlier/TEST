from flask_sqlalchemy import Pagination
from sqlalchemy import or_, and_

from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.app_name import App
from app.common.search import sort_query
from app.copro.cadastre import Cadastre
from app.copro.copros.exceptions import (
    CoproNotFoundException,
    MissionNotTypeCoproException,
    WrongCoproTypeException,
    WrongConstructionTimeException,
)
from app.copro.copros.interface import CoproInterface
from app.copro.copros.model import Copro
from app.copro.moe.model import Moe
from app.copro.moe.service import MoeService
from app.copro.president import President
from app.copro.president.service import PresidentService
from app.copro.syndic.service import SyndicService
from app.mission.missions.service import MissionService
from app.referential.enums.service import AppEnumService

COPRO_DEFAULT_PAGE = 1
COPRO_DEFAULT_PAGE_SIZE = 20
COPRO_DEFAULT_SORT_FIELD = "created_at"
COPRO_DEFAULT_SORT_DIRECTION = "desc"
COPRO_TYPE_ENUM = "CoproType"
CONSTRUCTION_TIME_ENUM = "ConstructionTime"
ENUMS = [COPRO_TYPE_ENUM, CONSTRUCTION_TIME_ENUM]


class CoproService:
    @staticmethod
    def get_all(
        page=COPRO_DEFAULT_PAGE,
        size=COPRO_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=COPRO_DEFAULT_SORT_FIELD,
        direction=COPRO_DEFAULT_SORT_DIRECTION,
        mission_id=None,
    ) -> Pagination:

        q = sort_query(Copro.query, sort_by, direction)
        q = q.filter(or_(Copro.is_deleted == False, Copro.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.join(
                Address,
                or_(Copro.address_1_id == Address.id, Copro.address_2_id == Address.id),
            ).filter(
                or_(
                    Copro.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if mission_id is not None:
            q = q.filter(Copro.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: CoproInterface) -> Copro:

        CoproService.check_enums(new_attrs)

        mission = MissionService.get_by_id(new_attrs.get("mission_id"))
        if mission.mission_type != App.COPRO:
            raise MissionNotTypeCoproException

        if new_attrs.get("address_1"):
            new_attrs["address_1_id"] = AddressService.create_address(
                new_attrs.get("address_1")
            )
            del new_attrs["address_1"]

        if new_attrs.get("address_2"):
            new_attrs["address_2_id"] = AddressService.create_address(
                new_attrs.get("address_2")
            )
            del new_attrs["address_2"]

        syndics = None
        if new_attrs.get("syndics"):
            syndics = new_attrs.get("syndics")
            del new_attrs["syndics"]

        cadastres = None
        if new_attrs.get("cadastres"):
            cadastres = new_attrs.get("cadastres")
            del new_attrs["cadastres"]

        if new_attrs.get("moe"):
            new_attrs["moe_id"] = MoeService.create(new_attrs.get("moe"))
            del new_attrs["moe"]

        new_attrs["president_id"] = PresidentService.create(
            new_attrs.get("president", {})
        )
        if new_attrs.get("president"):
            del new_attrs["president"]

        new_copro = Copro(**new_attrs)
        db.session.add(new_copro)
        db.session.commit()

        if cadastres:
            for c in cadastres:
                c["copro_id"] = new_copro.id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

        if syndics:
            for s in syndics:
                s["copro_id"] = new_copro.id
                SyndicService.create(s)

        return new_copro

    @staticmethod
    def get(copro_id) -> Copro:
        db_copro = Copro.query.get(copro_id)

        if db_copro is None:
            raise CoproNotFoundException

        return db_copro

    @staticmethod
    def update(db_copro: Copro, changes: CoproInterface, copro_id: int) -> Copro:

        CoproService.check_enums(changes)

        if changes.get("president"):
            PresidentService.update(
                President.query.get(db_copro.president_id), changes.get("president")
            )
            del changes["president"]

        if changes.get("cadastres"):
            delete_cadastres = Cadastre.__table__.delete().where(
                Cadastre.copro_id == copro_id
            )
            db.session.execute(delete_cadastres)
            db.session.commit()

            for c in changes.get("cadastres"):
                c["copro_id"] = copro_id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

            del changes["cadastres"]

        if changes.get("address_1"):
            if not db_copro.address_1_id:
                changes["address_1_id"] = AddressService.create_address(
                    changes.get("address_1")
                )
            else:
                AddressService.update_address(
                    db_copro.address_1_id, changes.get("address_1")
                )
            del changes["address_1"]

        if changes.get("address_2"):
            if not db_copro.address_2_id:
                changes["address_2_id"] = AddressService.create_address(
                    changes.get("address_2")
                )
            else:
                AddressService.update_address(
                    db_copro.address_1_id, changes.get("address_2")
                )
            del changes["address_2"]

        if changes.get("user_in_charge"):
            changes["user_in_charge_id"] = changes.get("user_in_charge").get("id")
            del changes["user_in_charge"]

        if changes.get("moe"):
            if not db_copro.moe_id:
                changes["moe_id"] = MoeService.create(changes.get("moe"))
            else:
                MoeService.update(Moe.query.get(db_copro.moe_id), changes.get("moe"))
            del changes["moe"]

        db_copro.update(changes)
        db.session.commit()

        return db_copro

    @staticmethod
    def delete(copro_id: int):
        current_copro = CoproService.get(copro_id)
        if current_copro:
            current_copro.soft_delete()
            db.session.commit()
        return copro_id

    @staticmethod
    def check_enums(payload: CoproInterface):
        enums = AppEnumService.get_enums(ENUMS)
        if payload.get("copro_type") is not None and payload.get(
            "copro_type"
        ) not in enums.get(COPRO_TYPE_ENUM):
            raise WrongCoproTypeException

        if payload.get("construction_time") is not None and payload.get(
            "construction_time"
        ) not in enums.get(CONSTRUCTION_TIME_ENUM):
            raise WrongConstructionTimeException
        return
