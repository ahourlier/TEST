from flask_sqlalchemy import Pagination
from flask_accepts import accepts, responds
from flask_allows import requires
from flask import request, jsonify, Response, g

from app.common.permissions import (
    has_mission_permission, is_contributor, has_combined_structure_permissions
)
from .schema import CombinedStructureSchema, CombinedStructurePaginatedSchema, CombinedStructureCreateSchema, CombinedStructureUpdateSchema
from .service import SEARCH_COMBINED_STRUCTURES_PARAMS, CombinedStructureService, COMBINED_STRUCTURE_DEFAULT_PAGE, COMBINED_STRUCTURE_DEFAULT_PAGE_SIZE, \
    COMBINED_STRUCTURE_DEFAULT_SORT_FIELD, COMBINED_STRUCTURE_DEFAULT_SORT_DIRECTION
from ..common.api import AuthenticatedApi
from . import api, CombinedStructure
from ..thematique.schema import ThematiqueMissionSchema


@api.route("")
class CombinedStructuresResource(AuthenticatedApi):
    """ CombinedStructures """

    @accepts(
        *SEARCH_COMBINED_STRUCTURES_PARAMS, api=api,
    )
    @responds(schema=CombinedStructurePaginatedSchema(), api=api)
    @requires(has_mission_permission)
    def get(self) -> Pagination:
        return CombinedStructureService.list(
            page=int(request.args.get("page", COMBINED_STRUCTURE_DEFAULT_PAGE)),
            size=int(request.args.get("size", COMBINED_STRUCTURE_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", COMBINED_STRUCTURE_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", COMBINED_STRUCTURE_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
            user=g.user
        )

    @accepts(schema=CombinedStructureCreateSchema(), api=api)
    @responds(schema=CombinedStructureSchema(), api=api)
    @requires(has_mission_permission, is_contributor)
    def post(self) -> CombinedStructure:
        return CombinedStructureService.create(request.parsed_obj)


@api.route("/<int:cs_id>")
@api.param("combined_structureId", "CombinedStructure unique id")
class CombinedStructuresResource(AuthenticatedApi):

    @responds(schema=CombinedStructureSchema(), api=api)
    @requires(has_combined_structure_permissions)
    def get(self, cs_id):
        return CombinedStructureService.get(cs_id)

    @responds(schema=CombinedStructureSchema(), api=api)
    @accepts(schema=CombinedStructureUpdateSchema(), api=api)
    @requires(has_combined_structure_permissions, is_contributor)
    def put(self, cs_id):
        db_combined_structure = CombinedStructureService.get(cs_id)
        return CombinedStructureService.update(db_combined_structure, cs_id, request.parsed_obj)

    @requires(has_combined_structure_permissions, is_contributor)
    def delete(self, cs_id) -> Response:
        deleted_id = CombinedStructureService.delete(cs_id)
        return jsonify(dict(status="Success", id=deleted_id))


@api.route("/<int:cs_id>/thematiques")
@api.param("combined_structureId", "CombinedStructure unique ID")
class CombinedStructureIdThematiqueResource(AuthenticatedApi):

    @responds(schema=ThematiqueMissionSchema(many=True), api=api)
    @requires(has_combined_structure_permissions)
    def get(self, cs_id: int):
        return CombinedStructureService.get_thematiques(cs_id)
