BASE_ROUTE = "referential"


def register_routes(api, app, root="api"):
    from .enums.controller import api as enums_api

    api.add_namespace(enums_api, path=f"/{root}/{BASE_ROUTE}/enums")
