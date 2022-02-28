from flask_restx import Namespace
from .model import Imports
from app.v2_imports.internal_controller import ImportRunView


BASE_ROUTE = "imports"

api = Namespace("Imports", description="Imports namespace")


def register_routes(api, app, root="api"):
    from .controller import api as imports_api

    api.add_namespace(imports_api, path=f"/{root}/{BASE_ROUTE}")


def register_internal_routes(bp):
    prefix = "/imports"
    bp.add_url_rule(
        f"{prefix}/run",
        view_func=ImportRunView.as_view("import-run"),
        methods=["PUT"],
    )
