from flask_restx import Namespace

from .model import Lot

BASE_ROUTE = "lots"

api = Namespace("Lot", description="Lots namespace")


def register_routes(api, app, root="api"):
    from .controller import api as lot_api

    api.add_namespace(lot_api, path=f"/{root}/{BASE_ROUTE}")
