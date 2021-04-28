BASE_ROUTE = "admin"

from .clients.model import Client


def register_routes(api, app, root="api"):
    from .agencies.controller import api as agencies_api
    from .antennas.controller import api as antennas_api
    from .clients.controller import api as clients_api

    api.add_namespace(agencies_api, path=f"/{root}/{BASE_ROUTE}/agencies")
    api.add_namespace(antennas_api, path=f"/{root}/{BASE_ROUTE}/antennas")
    api.add_namespace(clients_api, path=f"/{root}/{BASE_ROUTE}/clients")
