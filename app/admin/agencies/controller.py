from flask import request, Response, jsonify
from flask_accepts import responds, accepts
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import AgencySchema, api
from .interface import AgencyInterface
from .model import Agency
from .schema import AgencyPaginatedSchema
from .service import (
    AgencyService,
    AGENCIES_DEFAULT_PAGE,
    AGENCIES_DEFAULT_PAGE_SIZE,
    AGENCIES_DEFAULT_SORT_DIRECTION,
    AGENCIES_DEFAULT_SORT_FIELD,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import is_admin
from ...common.search import SEARCH_PARAMS


@api.route("/")
class AgencyResource(AuthenticatedApi):
    """Agencies"""

    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=AgencyPaginatedSchema())
    def get(self) -> Pagination:
        """Get all agencies"""
        return AgencyService.get_all(
            page=int(request.args.get("page", AGENCIES_DEFAULT_PAGE)),
            size=int(request.args.get("size", AGENCIES_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", AGENCIES_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", AGENCIES_DEFAULT_SORT_DIRECTION
            ),
        )

    @accepts(schema=AgencySchema, api=api)
    @responds(schema=AgencySchema)
    @requires(is_admin)
    def post(self) -> Agency:
        """Create an agency"""

        return AgencyService.create(request.parsed_obj)


@api.route("/<int:agency_id>")
@api.param("agencyId", "Agency unique ID")
class AgencyIdResource(AuthenticatedApi):
    @responds(schema=AgencySchema)
    def get(self, agency_id: int) -> Agency:
        """Get single agency"""

        return AgencyService.get_by_id(agency_id)

    @requires(is_admin)
    def delete(self, agency_id: int) -> Response:
        """Delete single agency"""

        id = AgencyService.delete_by_id(agency_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=AgencySchema, api=api)
    @responds(schema=AgencySchema)
    @requires(is_admin)
    def put(self, agency_id: int) -> Agency:
        """Update single agency"""

        changes: AgencyInterface = request.parsed_obj
        db_agency = AgencyService.get_by_id(agency_id)
        return AgencyService.update(db_agency, changes)
