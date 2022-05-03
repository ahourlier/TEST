from sqlalchemy import or_, and_

from app import db
from app.cle_repartition.model import CleRepartition
from app.combined_structure.error_handlers import (
    CombinedStructureNotFoundException,
    EnumException as CombinedStructureEnumException,
)
from app.combined_structure.interface import CombinedStructureInterface
from app.combined_structure.model import CombinedStructure
from app.common.address.schema import AddressSchema
from app.common.exceptions import EnumException
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.common.db_utils import DBUtils
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

ENUM_MAPPING = {"type": {"enum_key": "CombinedStructureType"}}


class CombinedStructureService:
    @staticmethod
    def list(
        page=COMBINED_STRUCTURE_DEFAULT_PAGE,
        size=COMBINED_STRUCTURE_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=COMBINED_STRUCTURE_DEFAULT_SORT_FIELD,
        direction=COMBINED_STRUCTURE_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        user=None,
    ):
        q = sort_query(CombinedStructure.query, sort_by, direction)
        q = q.filter(
            or_(
                CombinedStructure.is_deleted == False,
                CombinedStructure.is_deleted == None,
            )
        )
        if term not in [None, ""]:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    CombinedStructure.name.ilike(search_term),
                    CombinedStructure.type.ilike(search_term),
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
                enum=e.details.get("enum"),
            )

        new_attrs = CombinedStructureService.parse_payload(new_attrs)

        new_attrs["president_id"] = PresidentService.create(
            new_attrs.get("president", {})
        )
        if "president" in new_attrs:
            del new_attrs["president"]

        syndics = None
        if "syndics" in new_attrs:
            syndics = new_attrs.get("syndics", [])
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
        combined_structure = (
            CombinedStructure.query.filter(
                CombinedStructure.id == combined_structure_id
            )
            .filter(CombinedStructure.is_deleted == False)
            .first()
        )

        if not combined_structure:
            raise CombinedStructureNotFoundException

        return combined_structure

    @staticmethod
    def update(
        db_combined_structure: CombinedStructure,
        combined_structure_id: int,
        changes: CombinedStructureInterface,
    ):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise CombinedStructureEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        changes = CombinedStructureService.parse_payload(changes)

        if "president" in changes:
            PresidentService.update(
                PresidentService.get(db_combined_structure.president_id),
                changes.get("president"),
            )
            del changes["president"]

        if "syndics" in changes:
            del changes["syndics"]

        db_combined_structure.update(changes)
        db.session.commit()
        return db_combined_structure

    @staticmethod
    def delete(combined_structure_id):
        DBUtils.soft_delete_cascade(combined_structure_id, CombinedStructureService)
        return combined_structure_id

    @staticmethod
    def get_tantiemes_for_cs(cs):
        items = []
        address_schema = AddressSchema()
        for copro in cs.copros:
            item = {
                "copro": {
                    "name": copro.name,
                    "address_1": address_schema.dump(copro.address_1),
                }
            }
            tantieme = 0
            for lot in copro.lots:
                for cle in lot.cles_repartition:
                    tantieme += cle.tantieme
            item["tantieme"] = tantieme
            items.append(item)
        return items

    @staticmethod
    def get_sum_tantiemes_by_label(cs):
        sum_tantieme = {}

        # Define repartition keys for each copro in cs
        for copro in cs.copros:
            print(copro.id)
            cles = CleRepartition.query.filter(
                Copro.id == copro.id
            ).all()
            for cle in cles:
                sum_tantieme[cle.label] = None

        # Fill tantiemes for key repartition defined in lot
        for copro in cs.copros:
            for lot in copro.lots:
                for lot_cle in lot.cles_repartition:
                    cle = CleRepartition.query.filter(
                        CleRepartition.id == lot_cle.cle_repartition_id
                    ).first()
                    if cle.label in sum_tantieme and sum_tantieme[cle.label] == None:
                        sum_tantieme[cle.label] = 0
                    sum_tantieme[cle.label] += lot_cle.tantieme

        return sum_tantieme

    @staticmethod
    def get_thematiques(copro_id: int):
        combined_structure = CombinedStructureService.get(copro_id)
        return ThematiqueService.get_thematiques_from_mission(
            combined_structure.copro.mission_id
        )

    @staticmethod
    def parse_payload(payload):
        if (
            "account_closing_date" in payload
            and payload.get("account_closing_date") is not None
            and payload.get("account_closing_date").count("-") == 1
        ):
            payload["account_closing_date"] = f"{payload['account_closing_date']}-01"
        return payload
