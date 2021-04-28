from flask import request, Response, jsonify

from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Accommodation
from .interface import AccommodationInterface
from .schema import AccommodationSchema, AccommodationPaginatedSchema
from .service import (
    AccommodationService,
    ACCOMMODATIONS_DEFAULT_PAGE,
    ACCOMMODATIONS_DEFAULT_PAGE_SIZE,
    ACCOMMODATIONS_DEFAULT_SORT_FIELD,
    ACCOMMODATIONS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class AccommodationResource(AuthenticatedApi):
    """ accommodation api """

    @accepts(*SEARCH_PARAMS, dict(name="project_id", type=int), api=api)
    @responds(schema=AccommodationPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all accommodations """
        return AccommodationService.get_all(
            page=int(request.args.get("page", ACCOMMODATIONS_DEFAULT_PAGE)),
            size=int(request.args.get("size", ACCOMMODATIONS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", ACCOMMODATIONS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", ACCOMMODATIONS_DEFAULT_SORT_DIRECTION
            ),
            project_id=int(request.args.get("project_id"))
            if request.args.get("project_id") not in [None, ""]
            else None,
        )


@api.route("/project/<int:project_id>")
@api.param("projectId", "Project unique ID")
class AccommodationCreateResource(AuthenticatedApi):
    @accepts(schema=AccommodationSchema(), api=api)
    @responds(schema=AccommodationSchema(), api=api)
    def post(self, project_id) -> Accommodation:
        """ Create an accommodation """
        return AccommodationService.create(request.parsed_obj, project_id)


@api.route("/<int:accommodation_id>")
@api.param("accommodationId", "Accommodation unique ID")
class AccommodationIdResource(AuthenticatedApi):
    @responds(schema=AccommodationSchema(), api=api)
    def get(self, accommodation_id: int) -> Accommodation:
        """ Get single accommodation """

        return AccommodationService.get_by_id(accommodation_id)

    def delete(self, accommodation_id: int) -> Response:
        """Delete single accommodation"""

        id = AccommodationService.delete_by_id(accommodation_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=AccommodationSchema(), api=api)
    @responds(schema=AccommodationSchema(), api=api)
    def put(self, accommodation_id: int) -> Accommodation:
        """Update single accommodation"""

        changes: AccommodationInterface = request.parsed_obj
        db_accommodation = AccommodationService.get_by_id(accommodation_id)
        return AccommodationService.update(db_accommodation, changes)
