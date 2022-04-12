from flask import request
from flask_accepts import responds, accepts
from flask_sqlalchemy import Pagination

from app.auth.users import UserSchema
from app.auth.users.schema import UserPaginatedSchema
from app.common.api import AuthenticatedApi
from app.common.search import SEARCH_PARAMS
from app.project.project_leads import api
from app.project.project_leads.service import (
    ProjectLeadService,
    REFERRERS_DEFAULT_PAGE,
    REFERRERS_DEFAULT_PAGE_SIZE,
    REFERRERS_DEFAULT_SORT_FIELD,
    REFERRERS_DEFAULT_SORT_DIRECTION,
)


@api.route("/")
class ReferrersResource(AuthenticatedApi):
    """Referrers"""

    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=UserPaginatedSchema())
    def get(self) -> Pagination:
        """Get all referrers"""
        return ProjectLeadService.get_all(
            page=int(request.args.get("page", REFERRERS_DEFAULT_PAGE)),
            size=int(request.args.get("size", REFERRERS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", REFERRERS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", REFERRERS_DEFAULT_SORT_DIRECTION
            ),
        )
