from flask_accepts import responds, accepts
from flask import request, Response, jsonify

from app.common.api import AuthenticatedApi
from . import api
from .schema import SubcontractorSchema, SubcontractorPaginatedSchema
from .service import (
    SubcontractorService,
    SUBCONTRACTORS_DEFAULT_SORT_DIRECTION,
    SUBCONTRACTORS_DEFAULT_PAGE,
    SUBCONTRACTORS_DEFAULT_SORT_FIELD,
    SUBCONTRACTORS_DEFAULT_PAGE_SIZE,
)
from ...common.search import SEARCH_PARAMS


@api.route("")
class SubcontractorResource(AuthenticatedApi):
    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=SubcontractorPaginatedSchema, api=api)
    def get(self):
        return SubcontractorService.list(
            page=int(request.args.get("page", SUBCONTRACTORS_DEFAULT_PAGE)),
            size=int(request.args.get("size", SUBCONTRACTORS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", SUBCONTRACTORS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", SUBCONTRACTORS_DEFAULT_SORT_DIRECTION
            ),
        )

    @accepts(schema=SubcontractorSchema, api=api)
    @responds(schema=SubcontractorSchema, api=api)
    def post(self):
        return SubcontractorService.create(request.parsed_obj)


@api.route("/<subcontractor_id>")
@api.param("subcontractorId", "Subcontractor unique ID")
class SubcontractorIdResource(AuthenticatedApi):
    @responds(schema=SubcontractorSchema, api=api)
    def get(self, subcontractor_id: int):
        return SubcontractorService.get(subcontractor_id)

    @accepts(schema=SubcontractorSchema, api=api)
    @responds(schema=SubcontractorSchema, api=api)
    def put(self, subcontractor_id: int):
        db_subcontractor = SubcontractorService.get(subcontractor_id)
        return SubcontractorService.update(db_subcontractor, request.parsed_obj)

    def delete(self, subcontractor_id: int) -> Response:
        id = SubcontractorService.delete(subcontractor_id)
        return jsonify(dict(status="Success", id=id))
