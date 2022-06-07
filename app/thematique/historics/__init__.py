from flask_restx import Namespace
from .model import Historic
from .schema import HistoricSchema

BASE_ROUTE = "historics"

api = Namespace("Historics", description="Historic namespace")


def register_routes(api, app, root="api"):
    from .controller import api as historics_api

    api.add_namespace(historics_api, path=f"/{root}/{BASE_ROUTE}")
