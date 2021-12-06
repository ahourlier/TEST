from flask_restx import Namespace

from .model import Building

BASE_ROUTE = "buildings"

api = Namespace("Buildings", description="Buildings namespace")


def register_routes(api, app, root="api"):
    from .controller import api as building_api

    api.add_namespace(building_api, path=f"/{root}/{BASE_ROUTE}")
