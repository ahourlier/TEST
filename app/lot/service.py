from typing import List

from sqlalchemy import or_

from app import db
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.copro.copros.model import Copro
from app.lot import Lot
from app.lot.exceptions import LotNotFoundException, LotEnumException
from app.lot.interface import LotInterface
from app.person.service import PersonService

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
    ):
        q = sort_query(Lot.query, sort_by, direction)
        q = q.filter(or_(Lot.is_deleted == False, Lot.is_deleted == None))

        if copro_id:
            q = q.filter(Lot.copro_id == copro_id)

        if building_id:
            q = q.filter(Lot.building_id == building_id)

        if mission_id:
            q = q.join(Copro).filter(Copro.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: LotInterface):
        ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        if new_attrs.get("occupants") is not None:
            new_attrs["occupants"] = LotService.handle_occupants(new_attrs.get("occupants", []))
        new_lot = Lot(**new_attrs)
        db.session.add(new_lot)
        db.session.commit()
        return new_lot

    @staticmethod
    def get(lot_id: int):
        lot = Lot.query.get(lot_id)
        if not lot or lot.is_deleted:
            raise LotNotFoundException
        return lot

    @staticmethod
    def update(db_lot: Lot, changes: LotInterface):
        ServicesUtils.check_enums(changes, ENUM_MAPPING)

        if changes.get("occupants") is not None:
            db_lot.occupants = LotService.handle_occupants(changes.get("occupants", []))
            del changes["occupants"]

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
