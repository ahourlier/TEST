# from .model import ThematiqueEntity
from .model import ThematiqueMission
from flask_restx import Namespace


BASE_ROUTE = "thematiques"

api = Namespace("Thematique", description="Thematique namespace")


def register_routes(api, app, root="api"):
    from .controller import api as thematiques_api

    api.add_namespace(thematiques_api, path=f"/{root}/{BASE_ROUTE}")
