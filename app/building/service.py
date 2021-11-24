from sqlalchemy import or_, and_

from app import db
from app.building.exceptions import BuildingNotFoundException, WrongConstructionTimeException, \
    WrongERPCategoryException, WrongAccessTypeException, WrongCollectiveHeaterException, \
    WrongAsbestosDiagnosisResultException
from app.building.interface import BuildingInterface
from app.building.model import Building
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.copro.copros.model import Copro

SEARCH_BUILDINGS_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=int),
    dict(name="coproId", type=int),
]

BUILDING_DEFAULT_PAGE = 1
BUILDING_DEFAULT_PAGE_SIZE = 20
BUILDING_DEFAULT_SORT_FIELD = "created_at"
BUILDING_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "construction_time": {
        "enum_key": "BuildingConstructionTime",
        "exception": WrongConstructionTimeException
    },
    "erp_category": {
        "enum_key": "BuildingERPCategory",
        "exception": WrongERPCategoryException
    },
    "access_type": {
        "enum_key": "AccessType",
        "exception": WrongAccessTypeException
    },
    "collective_heater": {
        "enum_key": "CollectiveHeater",
        "exception": WrongCollectiveHeaterException
    },
    "asbestos_diagnosis_result": {
        "enum_key": "AsbestosDiagnosisResult",
        "exception": WrongAsbestosDiagnosisResultException
    }
}


class BuildingService:

    @staticmethod
    def list(
            page=BUILDING_DEFAULT_PAGE,
            size=BUILDING_DEFAULT_PAGE_SIZE,
            term=None,
            sort_by=BUILDING_DEFAULT_SORT_FIELD,
            direction=BUILDING_DEFAULT_SORT_DIRECTION,
            mission_id=None,
            copro_id=None,
    ):
        q = sort_query(Building.query, sort_by, direction)
        q = q.filter(or_(Building.is_deleted == False, Building.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.join(
                Address,
            ).filter(
                or_(
                    Building.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if copro_id:
            q = q.filter(Building.copro_id == copro_id)

        if mission_id:
            q = q.join(Copro).filter(Copro.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: BuildingInterface):

        ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)

        if new_attrs.get("address"):
            new_attrs["address_id"] = AddressService.create_address(new_attrs.get("address"))
            del new_attrs["address"]

        new_building = Building(**new_attrs)
        db.session.add(new_building)
        db.session.commit()
        return new_building

    @staticmethod
    def get(building_id) -> Building:
        building = Building.query.filter(Building.id == building_id).filter(Building.is_deleted == False).first()

        if not building:
            raise BuildingNotFoundException

        return building

    @staticmethod
    def update(db_building: Building, building_id: int, changes: BuildingInterface):

        ServicesUtils.check_enums(changes, ENUM_MAPPING)

        if changes.get("address"):
            if not db_building.address_id:
                changes["address_id"] = AddressService.create_address(changes.get("address"))
            else:
                AddressService.update_address(db_building.address_id, changes.get("address"))
            del changes["address"]

        db_building.update(changes)
        db.session.commit()
        return db_building

    @staticmethod
    def delete(building_id):
        existing_building = BuildingService.get(building_id)
        existing_building.soft_delete()
        db.session.commit()
        return building_id