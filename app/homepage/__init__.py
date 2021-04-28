BASE_ROUTE = "home"


def register_routes(api, app, root="api"):
    from .indicators.controller import api as indicators_api
    from .actions.controller import api as actions_api

    api.add_namespace(indicators_api, path=f"/{root}/{BASE_ROUTE}/indicator")
    api.add_namespace(actions_api, path=f"/{root}/{BASE_ROUTE}/actions")
