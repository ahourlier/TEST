from app.common.api import AuthenticatedApi
from flask_accepts import accepts, responds
from flask import request, jsonify, Response

from . import api, Elect
from .schema import ElectSchema, ElectUpdateSchema
from .service import ElectService


@api.route("")
class ElectResource(AuthenticatedApi):
    @accepts(schema=ElectSchema, api=api)
    @responds(schema=ElectSchema, api=api)
    def post(self):
        return ElectService.create(request.parsed_obj)


@api.route("/<int:elect_id>")
@api.param("electId", "Elect unique ID")
class ElectResource(AuthenticatedApi):
    @accepts(schema=ElectUpdateSchema, api=api)
    @responds(schema=ElectSchema, api=api)
    def put(self, elect_id: int):
        db_elect = ElectService.get_by_id(elect_id)
        return ElectService.update(db_elect, request.parsed_obj)

    def delete(self, elect_id: int) -> Response:
        id = ElectService.delete(elect_id)
        return jsonify(dict(status="Success", id=id))
