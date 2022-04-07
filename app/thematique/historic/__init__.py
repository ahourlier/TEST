BASE_ROUTE = "historic"


def register_routes(api, app, root="api"):
    from .historics.controller import api as historics_api

    api.add_namespace(historics_api, path=f"/{root}/{BASE_ROUTE}/historics")
