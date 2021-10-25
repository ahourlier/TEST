import logging

from flask import g, request
from flask_accepts import responds
from . import api, PreferredAppSchema
from .service import PreferredAppService

from ...common.api import AuthenticatedApi


@api.route("/preferred_app")
class PreferredApp(AuthenticatedApi):
    """ Current user profile """

    @responds(schema=PreferredAppSchema)
    def post(self):
        PreferredAppService.create(request.parsed_obj, g.user)
        return g.user

