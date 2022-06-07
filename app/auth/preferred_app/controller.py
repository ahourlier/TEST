from flask import g, request, jsonify, Response
from flask_accepts import responds, accepts
from flask_allows import requires

from . import api, PreferredAppSchema
from .service import PreferredAppService
from ..users import User

from ...common.api import AuthenticatedApi
from ...common.permissions import is_admin


@api.route("/me")
class PreferredAppMe(AuthenticatedApi):
    @responds(schema=PreferredAppSchema)
    def get(self):
        return PreferredAppService.get_my_preferred_app(g.user)


@api.route("/")
class PreferredApp(AuthenticatedApi):
    """Current preferred app"""

    @responds(schema=PreferredAppSchema)
    @accepts(schema=PreferredAppSchema, api=api)
    def post(self):
        return PreferredAppService.create(request.parsed_obj)


@api.route("/<int:preferred_app_id>")
@api.param("preferredAppId", "Preferred app unique id")
class PreferredAppId(AuthenticatedApi):
    @responds(schema=PreferredAppSchema)
    @accepts(schema=PreferredAppSchema, api=api)
    def put(self, preferred_app_id: int):
        return PreferredAppService.update(preferred_app_id, request.parsed_obj)

    @requires(is_admin)
    def delete(self, preferred_app_id: int) -> Response:
        PreferredAppService.delete(preferred_app_id)
        return jsonify(dict(status="Success", id=preferred_app_id))


@api.route("/user/<int:user_id>")
class PreferredAppUserId(AuthenticatedApi):
    @responds(schema=PreferredAppSchema)
    @accepts(schema=PreferredAppSchema, api=api)
    def post(self, user_id: int) -> User:
        return PreferredAppService.create_for_user(request.parsed_obj, user_id)
