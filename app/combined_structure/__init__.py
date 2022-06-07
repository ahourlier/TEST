from flask_restx import Namespace

from .model import CombinedStructure

BASE_ROUTE = "combined_structures"

api = Namespace("CombinedStructures", description="CombinedStructures namespace")


def register_routes(api, app, root="api"):
    from .controller import api as combined_structure_api

    api.add_namespace(combined_structure_api, path=f"/{root}/{BASE_ROUTE}")
