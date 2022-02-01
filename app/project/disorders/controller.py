from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, DisorderSchema, Disorder
from .interface import DisorderInterface
from .service import DisorderService
from ...common.api import AuthenticatedApi


@api.route("/")
class DisorderResource(AuthenticatedApi):
    """Disorders"""

    @accepts(schema=DisorderSchema, api=api)
    @responds(schema=DisorderSchema)
    def post(self) -> Disorder:
        """Create an disorder"""
        return DisorderService.create(request.parsed_obj)


@api.route("/<int:disorder_id>")
@api.param("disorderId", "Disorder unique ID")
class DisorderIdResource(AuthenticatedApi):
    def delete(self, disorder_id: int) -> Response:
        """Delete single disorder"""

        id = DisorderService.delete_by_id(disorder_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=DisorderSchema, api=api)
    @responds(schema=DisorderSchema)
    def put(self, disorder_id: int) -> Disorder:
        """Update single disorder"""
        changes: DisorderInterface = request.parsed_obj
        db_disorder = DisorderService.get_by_id(disorder_id)
        return DisorderService.update(db_disorder, changes)
