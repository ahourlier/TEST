from typing import List

from sqlalchemy import or_

from app import db
from app.auth.users.model import UserRole
from app.cle_repartition.service import CleRepartitionService
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.copro.copros.model import Copro
from app.lot import Lot
from app.lot.error_handlers import (
    LotNotFoundException,
    EnumException as LotEnumException,
)
from app.lot.interface import LotInterface
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

        q = sort_query(Lot.query, sort_by, direction)
        q = q.filter(or_(Lot.is_deleted == False, Lot.is_deleted == None))

        if copro_id:
            q = q.filter(Lot.copro_id == copro_id)

        if building_id:
            q = q.filter(Lot.building_id == building_id)

        if mission_id:
            q = q.join(Copro).filter(Copro.mission_id == mission_id)

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
            new_attrs["occupants"] = LotService.handle_occupants(
                new_attrs.get("occupants", [])
            )

        if "owner" in new_attrs:
            del new_attrs["owner"]

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
            db_lot.occupants = LotService.handle_occupants(changes.get("occupants", []))
            del changes["occupants"]

        if "owner" in changes:
            del changes["owner"]

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
        lot = LotService.get(lot_id)
        lot.soft_delete()
        db.session.commit()
        return lot_id

    @staticmethod
    def handle_occupants(list_dict_people: List[dict]):
        table = []
        for p in list_dict_people:
            table.append(PersonService.get(p.get("id")))
        return table

    @staticmethod
    def get_thematiques(lot_id: int):
        lot = LotService.get(lot_id)
        return ThematiqueService.get_thematiques_from_mission(lot.copro.mission_id)
