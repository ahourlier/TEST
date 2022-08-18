from typing import List

from sqlalchemy import or_

from app import db
from app.auth.users.model import UserRole
from app.building.model import Building
from app.cle_repartition.service import CleRepartitionService
from app.common.exceptions import EnumException
from app.common.phone_number.model import PhoneNumber
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.common.db_utils import DBUtils
from app.copro.copros.model import Copro
from app.common.address.model import Address
from app.auth.users.model import User
from app.lot import Lot
from app.lot.error_handlers import (
    LotNotFoundException,
    EnumException as LotEnumException,
    lot_not_found,
)
from app.lot.interface import LotInterface
from app.person.model import LotOwner, Person
from app.person.service import PersonService
from app.thematique.service import ThematiqueService

LOT_DEFAULT_PAGE = 1
LOT_DEFAULT_PAGE_SIZE = 20
LOT_DEFAULT_SORT_FIELD = "created_at"
LOT_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "type": {"enum_key": "LotType"},
    "habitation_type": {"enum_key": "LotHabitationType"},
    "occupant_status": {"enum_key": "LotOccupantStatus"},
    "lease_type": {"enum_key": "LotLeaseType"},
    "convention_rent_type": {"enum_key": "LotConventionRentType"},
}

MODEL_MAPPING = {
    "address": Address,
    "copro": Copro,
    "building": Building,
    "user_in_charge": User,
    "user": User,
    "person": Person,
    "phone_number": PhoneNumber,
}


class LotService:
    @staticmethod
    def list(
        page=LOT_DEFAULT_PAGE,
        size=LOT_DEFAULT_PAGE_SIZE,
        sort_by=LOT_DEFAULT_SORT_FIELD,
        direction=LOT_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        copro_id=None,
        building_id=None,
        cs_id=None,
        user=None,
    ):
        from app.mission.missions import Mission
        import app.mission.permissions as mission_permissions

        q = Lot.query
        if "." in sort_by:
            q = LotService.sort_from_sub_model(q, sort_by, direction)
        elif sort_by == "owners":
            q = LotService.sort_from_sub_model(q, "person.last_name", direction)
        else:
            q = sort_query(q, sort_by, direction)
            # Here to avoid multi join on Copro
            if mission_id:
                q = q.join(Copro).filter(Copro.mission_id == mission_id)

        q = q.filter(or_(Lot.is_deleted == False, Lot.is_deleted == None))

        if copro_id:
            q = q.filter(Lot.copro_id == copro_id)

        if building_id:
            q = q.filter(Lot.building_id == building_id)

        if cs_id:
            if not mission_id:
                q = q.join(Copro)
            q = q.filter(Copro.cs_id == cs_id)

        if user is not None and user.role != UserRole.ADMIN:
            if not mission_id and not cs_id:
                q = q.join(Copro)
            q = q.join(Mission)
            q = mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
                q, user
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: LotInterface):

        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise LotEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        if new_attrs.get("occupants") is not None:
            new_attrs["occupants"] = LotService.handle_persons(
                new_attrs.get("occupants", [])
            )

        if new_attrs.get("owners") is not None:
            new_attrs["owners"] = LotService.handle_persons(new_attrs.get("owners", []))

        links_cles = None
        if "cles_repartition" in new_attrs:
            links_cles = new_attrs.get("cles_repartition")
            del new_attrs["cles_repartition"]

        new_lot = Lot(**new_attrs)
        db.session.add(new_lot)
        db.session.commit()

        if links_cles:
            CleRepartitionService.handle_links(new_lot.id, links_cles)
        return new_lot

    @staticmethod
    def get(lot_id: int):
        lot = Lot.query.get(lot_id)
        if not lot or lot.is_deleted:
            raise LotNotFoundException
        return lot

    @staticmethod
    def update(db_lot: Lot, changes: LotInterface):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise LotEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        if changes.get("occupants") is not None:
            db_lot.occupants = LotService.handle_persons(changes.get("occupants", []))
            del changes["occupants"]

        if changes.get("owners") is not None:
            db_lot.owners = LotService.handle_persons(changes.get("owners", []))
            del changes["owners"]

        if "cles_repartition" in changes:
            CleRepartitionService.handle_links(
                db_lot.id, changes.get("cles_repartition")
            )
            del changes["cles_repartition"]

        db_lot.update(changes)
        db.session.commit()
        return db_lot

    @staticmethod
    def delete(lot_id: int):
        DBUtils.soft_delete_cascade(lot_id, LotService)
        return lot_id

    @staticmethod
    def handle_persons(list_dict_people: List[dict]):
        table = []
        for p in list_dict_people:
            table.append(PersonService.get(p.get("id")))
        return table

    @staticmethod
    def get_thematiques(lot_id: int):
        lot = LotService.get(lot_id)
        return ThematiqueService.get_thematiques_from_mission(lot.copro.mission_id)

    @staticmethod
    def search_by_unique_lot_number_in_copro(lot_number: str, copro: Copro):
        # Lot number is unique across copro
        return (
            Lot.query.filter(Lot.lot_number == lot_number)
            .filter(Lot.copro_id == copro.id)
            .filter(Lot.is_deleted == False)
            .first()
        )

    def sort_from_sub_model(query, sort_by, direction):
        values = sort_by.split(".")
        sub_model = MODEL_MAPPING[values[len(values) - 2]]
        if sub_model == Address:
            query = query.join(Copro)
            query = query.join(
                sub_model,
                or_(Copro.address_1_id == Address.id, Copro.address_2_id == Address.id),
                isouter=True
            )
        elif sub_model == User:
            query = query.join(Copro)
            query = query.join(
                User,
                Copro.user_in_charge_id == User.id,
                isouter=True
            )
        elif sub_model == Person:
            query = query.join(LotOwner)
            query = query.join(Person, LotOwner.c.owner_id == Person.id, isouter=True)
        elif sub_model == PhoneNumber:
            query = query.join(LotOwner)
            query = query.join(Person, LotOwner.c.owner_id == Person.id)
            query = query.join(PhoneNumber, Person.id == PhoneNumber.resource_id, isouter=True)
        else:
            query = query.join(sub_model, isouter=True)

        sort_by = values[len(values) - 1]

        return sort_query(query, sort_by, direction, sub_model)
