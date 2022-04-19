from flask_sqlalchemy import Pagination
from sqlalchemy import or_, and_

from app import db
from app.auth.users.model import UserRole
from app.cle_repartition.service import CleRepartitionService
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.app_name import App
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.common.db_utils import DBUtils
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.cadastre import Cadastre
from app.copro.copros.error_handlers import (
    CoproNotFoundException,
    MissionNotTypeCoproException,
    EnumException as CoproEnumException,
)
from app.copro.copros.interface import CoproInterface
from app.copro.copros.model import Copro
from app.copro.moe.model import Moe
from app.copro.moe.service import MoeService
from app.copro.president import President
from app.copro.president.service import PresidentService
from app.copro.syndic.service import SyndicService
from app.mission.missions.service import MissionService
from app.thematique.service import ThematiqueService

COPRO_DEFAULT_PAGE = 1
COPRO_DEFAULT_PAGE_SIZE = 20
COPRO_DEFAULT_SORT_FIELD = "created_at"
COPRO_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "copro_type": {"enum_key": "CoproType"},
    "construction_time": {"enum_key": "ConstructionTime"},
}


class CoproService:
    @staticmethod
    def get_all(
        page=COPRO_DEFAULT_PAGE,
        size=COPRO_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=COPRO_DEFAULT_SORT_FIELD,
        direction=COPRO_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        cs_id=None,
        user=None,
    ) -> Pagination:
        import app.mission.permissions as mission_permissions
        from app.mission.missions import Mission

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

        if cs_id is not None:
            q = q.filter(Copro.cs_id == cs_id)

        if user is not None and user.role != UserRole.ADMIN:
            q = q.join(Mission)
            q = mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
                q, user
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: CoproInterface) -> Copro:

        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise CoproEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

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

        if new_attrs.get("syndic_manager_address"):
            new_attrs["syndic_manager_address_id"] = AddressService.create_address(
                new_attrs.get("syndic_manager_address")
            )
            del new_attrs["syndic_manager_address"]

        if new_attrs.get("admin_manager_address"):
            new_attrs["admin_manager_address_id"] = AddressService.create_address(
                new_attrs.get("admin_manager_address")
            )
            del new_attrs["admin_manager_address"]

        phones = []
        if "syndic_manager_phone_number" in new_attrs:
            if new_attrs.get("syndic_manager_phone_number", None):
                phones.append(
                    PhoneNumber(**new_attrs.get("syndic_manager_phone_number"))
                )
            del new_attrs["syndic_manager_phone_number"]
        if "admin_manager_phone_number" in new_attrs:
            if new_attrs.get("admin_manager_phone_number", None):
                phones.append(
                    PhoneNumber(**new_attrs.get("admin_manager_phone_number"))
                )
            del new_attrs["admin_manager_phone_number"]
        new_attrs["phones"] = phones

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

        cles_repartition = None
        if "cles_repartition" in new_attrs:
            cles_repartition = new_attrs.get("cles_repartition")
            del new_attrs["cles_repartition"]

        try:
            new_copro = Copro(**new_attrs)
            db.session.add(new_copro)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise (e)

        if cadastres:
            for c in cadastres:
                c["copro_id"] = new_copro.id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

        if cles_repartition:
            CleRepartitionService.handle_keys(new_copro.id, cles_repartition)

        return new_copro

    @staticmethod
    def get(copro_id) -> Copro:
        db_copro = Copro.query.get(copro_id)

        if db_copro is None:
            raise CoproNotFoundException

        return db_copro

    @staticmethod
    def update(db_copro: Copro, changes: CoproInterface, copro_id: int) -> Copro:

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise CoproEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        if "president" in changes:
            if changes.get("president"):
                PresidentService.update(
                    President.query.get(db_copro.president_id), changes.get("president")
                )
            del changes["president"]
            del changes["president_id"]

        if "cadastres" in changes:
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

        if "address_1" in changes:
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

        if "address_2" in changes:
            if changes.get("address_2"):
                if not db_copro.address_2_id:
                    changes["address_2_id"] = AddressService.create_address(
                        changes.get("address_2")
                    )
                else:
                    AddressService.update_address(
                        db_copro.address_2_id, changes.get("address_2")
                    )
            del changes["address_2"]

        if "syndic_manager_address" in changes:
            if changes.get("syndic_manager_address"):
                if not db_copro.syndic_manager_address:
                    changes["syndic_manager_address"] = AddressService.create_address(
                        changes.get("syndic_manager_address")
                    )
                else:
                    AddressService.update_address(
                        db_copro.syndic_manager_address_id,
                        changes.get("syndic_manager_address"),
                    )
            del changes["syndic_manager_address"]

        if "admin_manager_address" in changes:
            if changes.get("admin_manager_address"):
                if not db_copro.admin_manager_address:
                    changes["admin_manager_address"] = AddressService.create_address(
                        changes.get("admin_manager_address")
                    )
                else:
                    AddressService.update_address(
                        db_copro.admin_manager_address_id,
                        changes.get("admin_manager_address"),
                    )
            del changes["admin_manager_address"]

        # Update phones numbers
        phones = []
        if "syndic_manager_phone_number" in changes:
            if changes["syndic_manager_phone_number"] is not None:
                phones.append(changes.get("syndic_manager_phone_number"))
            del changes["syndic_manager_phone_number"]
        if "admin_manager_phone_number" in changes:
            if changes["admin_manager_phone_number"] is not None:
                phones.append(changes.get("admin_manager_phone_number"))
            del changes["admin_manager_phone_number"]
        PhoneNumberService.update_phone_numbers(db_copro, phones)

        if "user_in_charge" in changes:
            if changes.get("user_in_charge"):
                changes["user_in_charge_id"] = changes.get("user_in_charge").get("id")
            del changes["user_in_charge"]

        if "moe" in changes:
            if changes.get("moe"):
                if not db_copro.moe_id:
                    changes["moe_id"] = MoeService.create(changes.get("moe"))
                else:
                    MoeService.update(
                        Moe.query.get(db_copro.moe_id), changes.get("moe")
                    )
            del changes["moe"]

        if "cles_repartition" in changes:
            CleRepartitionService.handle_keys(
                db_copro.id, changes.get("cles_repartition")
            )
            del changes["cles_repartition"]

        db_copro.update(changes)
        db.session.commit()

        return db_copro

    @staticmethod
    def delete(copro_id: int):
        DBUtils.soft_delete_cascade(copro_id, CoproService)
        return copro_id

    @staticmethod
    def get_thematiques(copro_id: int):
        copro = CoproService.get(copro_id)
        return ThematiqueService.get_thematiques_from_mission(copro.mission_id)

    @staticmethod
    def search_by_address(address_obj, mission_id):
        try:
            return (
                Copro.query.join(Address, Copro.address_1_id == Address.id)
                .filter(
                    and_(
                        Address.number == str(address_obj.get("number")),
                        Address.street == str(address_obj.get("street")),
                        Address.postal_code == str(address_obj.get("postal_code")),
                        Address.city == str(address_obj.get("city")),
                        Copro.mission_id == mission_id,
                        Copro.is_deleted == False,
                    )
                )
                .first()
            )
        except Exception as e:
            print(e)
