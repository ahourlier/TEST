import base64
from sqlalchemy import or_, and_, func

from app import db
from app.auth.users.model import UserRole
from app.building.error_handlers import BuildingNotFoundException, EnumException as BuildingEnumException
from app.building.interface import BuildingInterface
from app.building.model import Building
from app.building.settings import NB_LOOP_ACCESS_CODE
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.common.db_utils import DBUtils
from app.copro.copros.model import Copro
from app.thematique.service import ThematiqueService

SEARCH_BUILDINGS_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=int),
    dict(name="coproId", type=int),
    dict(name="csId", type=int),
]

BUILDING_DEFAULT_PAGE = 1
BUILDING_DEFAULT_PAGE_SIZE = 20
BUILDING_DEFAULT_SORT_FIELD = "created_at"
BUILDING_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "construction_time": {
        "enum_key": "BuildingConstructionTime"
    },
    "erp_category": {
        "enum_key": "BuildingERPCategory"
    },
    "access_type": {
        "enum_key": "AccessType"
    },
    "collective_heater": {
        "enum_key": "CollectiveHeater"
    },
    "asbestos_diagnosis_result": {
        "enum_key": "AsbestosDiagnosisResult"
    }
}

MODEL_MAPPING = {
    "copro": Copro,
    "address": Address
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
            cs_id=None,
            user=None
    ):
        from app.copro.copros import Copro
        from app.mission.missions import Mission
        import app.mission.permissions as mission_permissions

        q = Building.query
        if "." in sort_by:
            q = BuildingService.sort_from_sub_model(q, sort_by, direction)
        else:
            q = sort_query(q, sort_by, direction)

        q = q.filter(or_(Building.is_deleted == False, Building.is_deleted == None))

        if term not in [None, '']:
            search_term = f"%{term}%"
            q = q.outerjoin(
                Address,
                Building.address_id == Address.id
            ).filter(
                or_(
                    Building.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if copro_id:
            q = q.filter(Building.copro_id == int(copro_id))

        if mission_id:
            q = q.join(Copro, Building.copro_id == Copro.id).filter(Copro.mission_id == int(mission_id))
        
        if cs_id:
            if not mission_id:
                q = q.join(Copro, Building.address_id == Copro.address_1_id)
            q = q.filter(Copro.cs_id == cs_id)

        if user is not None and user.role != UserRole.ADMIN:
            # On Global Listing page and not admin, need copro to join with mission
            if not mission_id and not cs_id:
                q = q.join(Copro)

            q = q.join(Mission)
            q = mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
                q, user
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: BuildingInterface):
        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise BuildingEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if new_attrs.get("address"):
            new_attrs["address_id"] = AddressService.create_address(new_attrs.get("address"))
            del new_attrs["address"]

        if new_attrs.get("access_code"):
            new_attrs["access_code"] = BuildingService.encode_access_code(new_attrs.get("access_code"))

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
    def update(db_building: Building, changes: BuildingInterface):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise BuildingEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if changes.get("address"):
            if not db_building.address_id:
                changes["address_id"] = AddressService.create_address(changes.get("address"))
            else:
                AddressService.update_address(db_building.address_id, changes.get("address"))
            del changes["address"]

        if changes.get("access_code"):
            changes["access_code"] = BuildingService.encode_access_code(changes.get("access_code"))

        db_building.update(changes)
        db.session.commit()
        return db_building

    @staticmethod
    def delete(building_id):
        DBUtils.soft_delete_cascade(building_id, BuildingService)
        return building_id

    @staticmethod
    def encode_access_code(access_code):
        for i in range(0, NB_LOOP_ACCESS_CODE):
            if type(access_code) == str:
                access_code = access_code.encode("ascii")
            access_code = base64.b64encode(access_code)
        return access_code.decode()

    @staticmethod
    def get_thematiques(copro_id: int):
        building = BuildingService.get(copro_id)
        return ThematiqueService.get_thematiques_from_mission(building.copro.mission_id)

    @staticmethod
    def get_building_from_unique_name(building_name: str, copro: Copro):
        # Building name is unique across copro
        return Building.query.filter(Building.copro_id == copro.id) \
                             .filter(func.lower(Building.name) == func.lower(building_name)) \
                             .filter(Building.is_deleted == False) \
                             .first()
    
    def sort_from_sub_model(query, sort_by, direction):
        values = sort_by.split(".")
        sub_model = MODEL_MAPPING[values[0]]
        query = query.join(sub_model, isouter=True)
        sort_by = values[1]
        return sort_query(query, sort_by, direction, sub_model)
        