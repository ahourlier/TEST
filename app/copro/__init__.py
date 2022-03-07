BASE_ROUTE = "copro"


def register_routes(api, app, root="api"):
    from .copros.controller import api as copro_api
    from .syndic.controller import api as syndic_api

    api.add_namespace(copro_api, path=f"/{root}/{BASE_ROUTE}/copros")
    api.add_namespace(syndic_api, path=f"/{root}/{BASE_ROUTE}/syndic")
