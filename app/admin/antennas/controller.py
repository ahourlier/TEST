from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, AntennaSchema, Antenna
from .interface import AntennaInterface
from .schema import AntennaPaginatedSchema
from .service import (
    AntennaService,
    ANTENNAS_DEFAULT_PAGE,
    ANTENNAS_DEFAULT_PAGE_SIZE,
    ANTENNAS_DEFAULT_SORT_FIELD,
    ANTENNAS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import is_admin
from ...common.search import SEARCH_PARAMS


@api.route("/")
class AntennaResource(AuthenticatedApi):
    """Antennas"""

    @accepts(*SEARCH_PARAMS, dict(name="agency_id", type=int), api=api)
    @responds(schema=AntennaPaginatedSchema())
    def get(self) -> Pagination:
        """Get all antennas"""
        return AntennaService.get_all(
            page=int(request.args.get("page", ANTENNAS_DEFAULT_PAGE)),
            size=int(request.args.get("size", ANTENNAS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", ANTENNAS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", ANTENNAS_DEFAULT_SORT_DIRECTION
            ),
            agency_id=int(request.args.get("agency_id"))
            if request.args.get("agency_id") not in [None, ""]
            else None,
        )

    @accepts(schema=AntennaSchema, api=api)
    @responds(schema=AntennaSchema)
    @requires(is_admin)
    def post(self) -> Antenna:
        """Create an antenna"""
        return AntennaService.create(request.parsed_obj)


@api.route("/<int:antenna_id>")
@api.param("antennaId", "Antenna unique ID")
class AntennaIdResource(AuthenticatedApi):
    @responds(schema=AntennaSchema)
    def get(self, antenna_id: int) -> Antenna:
        """Get single antenna"""

        return AntennaService.get_by_id(antenna_id)

    @requires(is_admin)
    def delete(self, antenna_id: int) -> Response:
        """Delete single antenna"""

        id = AntennaService.delete_by_id(antenna_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=AntennaSchema, api=api)
    @responds(schema=AntennaSchema)
    @requires(is_admin)
    def put(self, antenna_id: int) -> Antenna:
        """Update single antenna"""

        changes: AntennaInterface = request.parsed_obj
        db_antenna = AntennaService.get_by_id(antenna_id)
        return AntennaService.update(db_antenna, changes)
