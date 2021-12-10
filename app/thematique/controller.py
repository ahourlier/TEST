from flask import Response, request
from flask_accepts import responds, accepts

from . import api
from .schema import Thematique, ThematiqueForObject, VersionCreate, Version
from .service import ThematiqueService
from ..common.api import AuthenticatedApi

THEMATIQUE_TEMPLATE_SEARCH_PARAMS = [
    dict(name="scope", type=str),
    dict(name="name", type=str),
]

THEMATIQUE_SEARCH_PARAMS = [dict(name="resourceId", type=int)]


@api.route("/templates")
class ThematiqueResource(AuthenticatedApi):
    """ Thematique """

    @responds(schema=Thematique(many=True), api=api)
    @accepts(*THEMATIQUE_TEMPLATE_SEARCH_PARAMS, api=api)
    def get(self):
        return ThematiqueService.list_templates(
            scope=request.args.get("scope")
            if request.args.get("scope") not in [None, ""]
            else None,
            name=request.args.get("name")
            if request.args.get("name") not in [None, ""]
            else None,
        )


@api.route("/duplicate")
class ThematiqueIdResource(AuthenticatedApi):
    @accepts(schema=Version, api=api)
    @responds(schema=Version, api=api)
    def post(self):
        return ThematiqueService.duplicate_thematique(request.parsed_obj)
