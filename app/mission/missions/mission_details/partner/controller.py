from app.common.api import AuthenticatedApi
from flask_accepts import accepts, responds
from flask import request, jsonify, Response

from . import api, Partner
from .schema import PartnerSchema, PartnerUpdateSchema
from .service import PartnerService


@api.route("/")
class PartnerResource(AuthenticatedApi):
    @accepts(schema=PartnerSchema, api=api)
    @responds(schema=PartnerSchema, api=api)
    def post(self):
        return PartnerService.create(request.parsed_obj)


@api.route("/<int:partner_id>")
@api.param("partnerId", "Partner unique ID")
class PartnerResource(AuthenticatedApi):
    @accepts(schema=PartnerUpdateSchema, api=api)
    @responds(schema=PartnerSchema, api=api)
    def put(self, partner_id: int):
        db_partner = PartnerService.get_by_id(partner_id)
        return PartnerService.update(db_partner, request.parsed_obj)

    def delete(self, partner_id: int) -> Response:
        id = PartnerService.delete(partner_id)
        return jsonify(dict(status="Success", id=id))
