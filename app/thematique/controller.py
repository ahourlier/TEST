from flask import request, jsonify, g
from flask_accepts import responds, accepts
from flask_allows import requires

from app.common.permissions import has_thematic_permissions, has_version_permissions
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
    @requires(has_thematic_permissions)
    def get(self):
        return ThematiqueService.list_versions(
            scope=request.args.get("scope"),
            resource_id=request.args.get("resourceId"),
            thematique_name=request.args.get("thematiqueName"),
        )


@api.route("/templates")
class ThematiqueResource(AuthenticatedApi):
    """Thematique"""

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
    @requires(has_version_permissions)
    def put(self, version_id: str, step_id: str):
        return ThematiqueService.update_step(
            version_id=version_id,
            step_id=step_id,
            payload=request.parsed_obj,
            user=g.user,
        )


@api.route("/duplicate")
class ThematiqueIdResource(AuthenticatedApi):
    @accepts(schema=VersionSchema, api=api)
    @responds(schema=VersionSchema, api=api)
    @requires(has_thematic_permissions)
    def post(self):
        return ThematiqueService.duplicate_thematique(request.parsed_obj)


@api.route("/<string:version_id>")
class ThematiqueIdResource(AuthenticatedApi):
    @accepts(schema=VersionSchema, api=api)
    @requires(has_version_permissions)
    def put(self, version_id):
        ThematiqueService.update_version(
            version_id=version_id,
            payload=request.json,
        )
        return jsonify(dict(status="Success", id=version_id))

    def delete(self, version_id):
        ThematiqueService.delete_copro_version(
            version_id=version_id,
        )
        return jsonify(dict(status="Success", id=version_id))
