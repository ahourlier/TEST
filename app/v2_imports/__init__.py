from flask_restx import Namespace

from .model import Imports

BASE_ROUTE = "imports"

api = Namespace("Imports", description="Imports namespace")


def register_routes(api, app, root="api"):
    from .controller import api as imports_api

    api.add_namespace(imports_api, path=f"/{root}/{BASE_ROUTE}")
