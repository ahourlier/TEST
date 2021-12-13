from flask import Response, request
from flask_accepts import responds, accepts

from . import api
from .schema import ThematiqueSchema, VersionSchema, StepSchema
from .service import ThematiqueService
from ..common.api import AuthenticatedApi

THEMATIQUE_TEMPLATE_SEARCH_PARAMS = [
    dict(name="scope", type=str),
    dict(name="name", type=str),
]

THEMATIQUE_SEARCH_PARAMS = [
    dict(name="resourceId", type=int),
    dict(name="scope", type=str),
    dict(name="thematiqueName", type=str),
]


@api.route("")
class ThematiqueForObjectResource(AuthenticatedApi):
    @accepts(*THEMATIQUE_SEARCH_PARAMS, api=api)
    @responds(schema=VersionSchema(many=True), api=api)
    def get(self):
        return ThematiqueService.list_versions(
            scope=request.args.get("scope"),
            resource_id=request.args.get("resourceId"),
            thematique_name=request.args.get("thematiqueName"),
        )


@api.route("/templates")
class ThematiqueResource(AuthenticatedApi):
    """ Thematique """

    @responds(schema=ThematiqueSchema(many=True), api=api)
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


@api.route("/<string:version_id>/step/<string:step_id>")
class ThematiqueStepResource(AuthenticatedApi):

    @accepts(schema=StepSchema, api=api)
    @responds(schema=VersionSchema, api=api)
    def put(self, version_id: str, step_id: str):
        return ThematiqueService.update_step(
            version_id=version_id,
            step_id=step_id,
            payload=request.parsed_obj
        )


@api.route("/duplicate")
class ThematiqueIdResource(AuthenticatedApi):
    @accepts(schema=VersionSchema, api=api)
    @responds(schema=VersionSchema, api=api)
    def post(self):
        return ThematiqueService.duplicate_thematique(request.parsed_obj)
