from flask import request
from flask_accepts import responds, accepts
from . import api

from .config_structure import ENTITY_TO_MODEL_MAPPING
from .schema import SearchItemsStructureSchema
from .service import SearchV2Service, StructureService

from ..mission.missions.schema import MissionPaginatedSchema
from ..lot.schema import LotPaginatedSchema
from ..building.schema import BuildingPaginatedSchema
from ..copro.copros.schema import CoproPaginatedSchema
from ..combined_structure.schema import CombinedStructurePaginatedSchema
from ..common.api import AuthenticatedApi


@api.route("/<entity>")
class SearchEntityResource(AuthenticatedApi):
    def get(self, entity):
        if entity not in ENTITY_TO_MODEL_MAPPING:
            return f"Entity {entity} has no model reference... Choose either 'mission', 'lot', 'building', 'copro' or 'combined_structure'"

        entity_schema_mapping = {
            "mission": MissionPaginatedSchema(),
            "lot": LotPaginatedSchema(),
            "building": BuildingPaginatedSchema(),
            "copro": CoproPaginatedSchema(),
            "combined_structure": CombinedStructurePaginatedSchema(),
        }
        parameters = request.args
        # Get association between column name and field to search in for one to one realtionships
        # ex: agency_id -> agency.name
        one_to_one_references = SearchV2Service.get_one_to_one_references_from_entity(
            entity
        )
        # Get list of matching entity
        results = SearchV2Service.search_entity(
            entity, one_to_one_references, parameters, "in"
        )
        schema = entity_schema_mapping[entity]
        return schema.dump({"items": results})


@api.route("/<entity>/structure")
class SearchEntityStructure(AuthenticatedApi):
    @responds(schema=SearchItemsStructureSchema(), api=api)
    def get(self, entity):
        structure = []
        structure = StructureService.build_structure(entity, structure)
        return {"entity": entity, "items": structure}
