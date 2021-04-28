BASE_ROUTE = "project"
from .requesters.model import Requester
from .projects import model
from .accommodations.model import Accommodation
from .common_areas.model import CommonArea
from .disorders import model
from .quotes.model import Quote
from .projects.controller import api as projects_api
from .accommodations.controller import api as accommodations_api
from .disorders.controller import api as disorders_api
from .search.controller import api as search_api
from .requesters.controller import api as requesters_api
from .project_leads.controller import api as referrers_api
from .comments.controller import api as comments_api
from .quotes.controller import api as quotes_api
from .work_types.model import WorkType
from .simulations.controller import api as simulations_api
from .simulations_uses.controller import api as simulations_uses_api
from .common_areas.controller import api as common_areas_api
from .project_custom_fields.controller import api as project_custom_fields_api
from .funders_monitoring_values.controller import api as funders_monitoring_values_api


def register_routes(api, app, root="api"):

    api.add_namespace(projects_api, path=f"/{root}/{BASE_ROUTE}/projects")
    api.add_namespace(accommodations_api, path=f"/{root}/{BASE_ROUTE}/accommodations")
    api.add_namespace(disorders_api, path=f"/{root}/{BASE_ROUTE}/disorders")
    api.add_namespace(search_api, path=f"/{root}/{BASE_ROUTE}/search")
    api.add_namespace(requesters_api, path=f"/{root}/{BASE_ROUTE}/requesters")
    api.add_namespace(referrers_api, path=f"/{root}/{BASE_ROUTE}/referrers")
    api.add_namespace(comments_api, path=f"/{root}/{BASE_ROUTE}/comments")
    api.add_namespace(quotes_api, path=f"/{root}/{BASE_ROUTE}/quotes")
    api.add_namespace(simulations_api, path=f"/{root}/{BASE_ROUTE}/simulations")
    api.add_namespace(
        simulations_uses_api, path=f"/{root}/{BASE_ROUTE}/simulations_use"
    )
    api.add_namespace(common_areas_api, path=f"/{root}/{BASE_ROUTE}/common_areas")
    api.add_namespace(
        project_custom_fields_api, path=f"/{root}/{BASE_ROUTE}/custom_fields"
    )
    api.add_namespace(
        funders_monitoring_values_api,
        path=f"/{root}/{BASE_ROUTE}/funders_monitoring_values",
    )


def register_internal_routes(bp):
    from .projects.internal_controller import (
        ProjectInitDriveView,
        ProjectDeleteFilesView,
    )

    prefix = "/projects"
    bp.add_url_rule(
        f"{prefix}/init-drive",
        view_func=ProjectInitDriveView.as_view("project-init-drive"),
        methods=["POST"],
    )
    bp.add_url_rule(
        f"{prefix}/delete-files",
        view_func=ProjectDeleteFilesView.as_view("delete-files"),
        methods=["POST"],
    )
