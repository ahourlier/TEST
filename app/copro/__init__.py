
BASE_ROUTE = "copro"


def register_routes(api, app, root="api"):
    from .copros import api as copro_api

    api.add_namespace(copro_api, path=f"/{root}/{BASE_ROUTE}/copros")

