from flask import request
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api
from .schema import HomepageActionsSchema
from .service import RequiredActionsService
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS
from ...project.projects.schema import ProjectPaginatedSchema
from ...project.projects.service import (
    PROJECTS_DEFAULT_PAGE,
    PROJECTS_DEFAULT_PAGE_SIZE,
    PROJECTS_DEFAULT_SORT_FIELD,
    PROJECTS_DEFAULT_SORT_DIRECTION,
)


@api.route("/")
class ActionsCountResource(AuthenticatedApi):
    @responds(schema=HomepageActionsSchema(), api=api)
    def get(self):
        """Get required actions data"""

        return RequiredActionsService.get_counts()


@api.route("/projects/")
class ActionsFetchProjectsResources(AuthenticatedApi):
    @accepts(
        *SEARCH_PARAMS, dict(name="alert_type", type=str), api=api,
    )
    @responds(schema=ProjectPaginatedSchema(), api=api)
    def get(self) -> Pagination:
        """Get projects corresponding to an alert type"""
        return RequiredActionsService.fetch_reported_projects(
            page=int(request.args.get("page", PROJECTS_DEFAULT_PAGE)),
            size=int(request.args.get("size", PROJECTS_DEFAULT_PAGE_SIZE)),
            sort_by=request.args.get("sortBy", PROJECTS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", PROJECTS_DEFAULT_SORT_DIRECTION
            ),
            alert_type=str(request.args.get("alert_type"))
            if request.args.get("alert_type") not in [None, ""]
            else None,
        )
