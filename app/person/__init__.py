from flask_restx import Namespace

from .model import Person

BASE_ROUTE = "person"

api = Namespace("Person", description="People namespace")


def register_routes(api, app, root="api"):
    from .controller import api as person_api

    api.add_namespace(person_api, path=f"/{root}/{BASE_ROUTE}")
