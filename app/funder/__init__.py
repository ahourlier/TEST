BASE_ROUTE = "funder"


def register_routes(api, app, root="api"):
    from .funders.controller import api as funders_api
    from .funding_scenarios.controller import api as funding_scenarios_api

    api.add_namespace(funders_api, path=f"/{root}/{BASE_ROUTE}/funders")
    api.add_namespace(
        funding_scenarios_api, path=f"/{root}/{BASE_ROUTE}/funding-scenarios"
    )
