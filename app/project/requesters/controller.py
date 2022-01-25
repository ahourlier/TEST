from flask import request, g
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api
from .schema import RequesterPaginatedSchema
from .service import (
    RequesterService,
    REQUESTERS_DEFAULT_PAGE,
    REQUESTERS_DEFAULT_PAGE_SIZE,
    REQUESTERS_DEFAULT_SORT_FIELD,
    REQUESTERS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class RequesterResource(AuthenticatedApi):
    """Requesters"""

    @accepts(
        *SEARCH_PARAMS,
        dict(name="agency_id", type=int),
        dict(name="type", type=str),
        dict(name="first_name", type=str),
        dict(name="last_name", type=str),
        dict(name="excluded_project", type=str),
        api=api,
    )
    @responds(schema=RequesterPaginatedSchema)
    def get(self) -> Pagination:
        """Get all requesters"""
        return RequesterService.get_all(
            page=int(request.args.get("page", REQUESTERS_DEFAULT_PAGE)),
            size=int(request.args.get("size", REQUESTERS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            first_name=request.args.get("first_name"),
            last_name=request.args.get("last_name"),
            sort_by=request.args.get("sortBy", REQUESTERS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", REQUESTERS_DEFAULT_SORT_DIRECTION
            ),
            type=str(request.args.get("type"))
            if request.args.get("type") not in [None, ""]
            else None,
            user=g.user,
            excluded_project=str(request.args.get("excluded_project"))
            if request.args.get("type") not in [None, ""]
            else None,
        )
