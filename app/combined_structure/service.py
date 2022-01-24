import base64

from sqlalchemy import or_, and_

from app import db
from app.auth.users.model import UserRole
from app.combined_structure.error_handlers import CombinedStructureNotFoundException, EnumException as CombinedStructureEnumException
from app.combined_structure.interface import CombinedStructureInterface
from app.combined_structure.model import CombinedStructure
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.copro.copros.model import Copro
from app.copro.president.service import PresidentService
from app.copro.syndic.service import SyndicService
from app.thematique.service import ThematiqueService

SEARCH_COMBINED_STRUCTURES_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=int),
]

COMBINED_STRUCTURE_DEFAULT_PAGE = 1
COMBINED_STRUCTURE_DEFAULT_PAGE_SIZE = 20
COMBINED_STRUCTURE_DEFAULT_SORT_FIELD = "created_at"
COMBINED_STRUCTURE_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "type": {
        "enum_key": "CombinedStructureType"
    }
}


class CombinedStructureService:

    @staticmethod
    def list(
            page=COMBINED_STRUCTURE_DEFAULT_PAGE,
            size=COMBINED_STRUCTURE_DEFAULT_PAGE_SIZE,
            term=None,
            sort_by=COMBINED_STRUCTURE_DEFAULT_SORT_FIELD,
            direction=COMBINED_STRUCTURE_DEFAULT_SORT_DIRECTION,
            mission_id=None,
            user=None
    ):
        q = sort_query(CombinedStructure.query, sort_by, direction)
        q = q.filter(or_(CombinedStructure.is_deleted == False, CombinedStructure.is_deleted == None))
        if term not in [None, '']:
            search_term = f"%{term}%"
            q = q.outerjoin(
                Address,
                CombinedStructure.address_id == Address.id
            ).filter(
                or_(
                    CombinedStructure.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if mission_id:
            q = q.filter(CombinedStructure.mission_id == int(mission_id))

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: CombinedStructureInterface):
        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise CombinedStructureEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if new_attrs.get("address"):
            new_attrs["address_id"] = AddressService.create_address(new_attrs.get("address"))
            del new_attrs["address"]
        
        new_attrs["president_id"] = PresidentService.create(
            new_attrs.get("president", {})
        )
        if new_attrs.get("president"):
            del new_attrs["president"]
        
        syndics = None
        if new_attrs.get("syndics"):
            syndics = new_attrs.get("syndics")
            del new_attrs["syndics"]

        new_combined_structure = CombinedStructure(**new_attrs)
        db.session.add(new_combined_structure)
        db.session.commit()

        if syndics:
            for s in syndics:
                s["cs_id"] = new_combined_structure.id
                SyndicService.create(s)
        return new_combined_structure

    @staticmethod
    def get(combined_structure_id) -> CombinedStructure:
        combined_structure = CombinedStructure.query.filter(CombinedStructure.id == combined_structure_id).filter(CombinedStructure.is_deleted == False).first()

        if not combined_structure:
            raise CombinedStructureNotFoundException

        return combined_structure

    @staticmethod
    def update(db_combined_structure: CombinedStructure, combined_structure_id: int, changes: CombinedStructureInterface):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise CombinedStructureEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if changes.get("address"):
            if not db_combined_structure.address_id:
                changes["address_id"] = AddressService.create_address(changes.get("address"))
            else:
                AddressService.update_address(db_combined_structure.address_id, changes.get("address"))
            del changes["address"]

        if changes.get("access_code"):
            changes["access_code"] = CombinedStructureService.encode_access_code(changes.get("access_code"))

        db_combined_structure.update(changes)
        db.session.commit()
        return db_combined_structure

    @staticmethod
    def delete(combined_structure_id):
        existing_combined_structure = CombinedStructureService.get(combined_structure_id)
        existing_combined_structure.soft_delete()
        db.session.commit()
        return combined_structure_id

    @staticmethod
    def get_thematiques(copro_id: int):
        combined_structure = CombinedStructureService.get(copro_id)
        return ThematiqueService.get_thematiques_from_mission(combined_structure.copro.mission_id)