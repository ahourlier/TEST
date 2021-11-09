from flask_accepts import responds, accepts
from flask import request, Response, jsonify

from app.common.api import AuthenticatedApi
from . import api
from .schema import SubcontractorSchema
from .service import SubcontractorService


@api.route("")
class SubcontractorResource(AuthenticatedApi):
    @responds(schema=SubcontractorSchema, many=True, api=api)
    def get(self):
        return SubcontractorService.list()

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
