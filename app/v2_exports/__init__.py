from flask_restx import Namespace
from app.v2_exports.internal_controller import ExportRunView


BASE_ROUTE = "exports"

api = Namespace("Exports", description="Exports namespace")


def register_routes(api, app, root="api"):
    from .controller import api as exports_api

    api.add_namespace(exports_api, path=f"/{root}/{BASE_ROUTE}")


def register_internal_routes(bp):
    prefix = "/exports"
    bp.add_url_rule(
        f"{prefix}/run",
        view_func=ExportRunView.as_view("export-run"),
        methods=["PUT"],
    )
