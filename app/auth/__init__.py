BASE_ROUTE = "auth"


def register_routes(api, app, root="api"):
    from .users.controller import api as users_api
    from .preferred_app.controller import api as preferred_app_api

    api.add_namespace(users_api, path=f"/{root}/{BASE_ROUTE}/users")
    api.add_namespace(preferred_app_api, path=f"/{root}/{BASE_ROUTE}/preferred_app")
