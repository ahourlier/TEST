from flask_restx import Namespace


BASE_ROUTE = "search"

api = Namespace("Search", description="Search namespace")


def register_routes(api, app, root="api"):
    from .controller import api as search_api

    api.add_namespace(search_api, path=f"/{root}/{BASE_ROUTE}")
