from flask import request, Response, jsonify
from flask_accepts import accepts, responds

from . import api
from .schema import EnumsFetchSchema, CompleteEnumSchema

from .service import AppEnumService, PerrenoudAppEnumService
from app.common.api import AuthenticatedApi


@api.route("/")
class AppEnumResource(AuthenticatedApi):
    """ Enums """

    @accepts(dict(name="enums", type=str), api=api)
    def get(self) -> Response:
        """ Get requested enums """
        enum_list = request.args.get("enums", "").split(",")
        return jsonify(AppEnumService.get_enums(enum_list))


@api.route("/perrenoud")
class PerrenoudEnumResource(AuthenticatedApi):
    """ Perrenoud Enums """

    @accepts(schema=EnumsFetchSchema())
    @responds(schema=CompleteEnumSchema(many=True))
    def put(self):
        """ Fetch all wanted perrenoud enums """
        return PerrenoudAppEnumService.get_perrenoud_enums(
            request.parsed_obj.get("enums")
        )
