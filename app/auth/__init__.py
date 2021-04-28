BASE_ROUTE = "auth"


def register_routes(api, app, root="api"):
    from .users.controller import api as users_api

    api.add_namespace(users_api, path=f"/{root}/{BASE_ROUTE}/users")
