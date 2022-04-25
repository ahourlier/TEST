from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Historic, HistoricSchema
from .schema import HistoricPaginatedSchema
from .service import HistoricService
from app.common.api import AuthenticatedApi

from .service import (
    HISTORICS_DEFAULT_PAGE,
    HISTORICS_DEFAULT_PAGE_SIZE,
    HISTORICS_DEFAULT_SORT_FIELD,
    HISTORICS_DEFAULT_SORT_DIRECTION
)

@api.route("/")
class HistoricResource(AuthenticatedApi):
    """Historics"""

    @accepts(api=api)
    @responds(schema=HistoricPaginatedSchema)
    def get(self) -> Pagination:
        """Get all historics"""
        return HistoricService.get_all(
            page=int(request.args.get("page")) if request.args.get("page") else HISTORICS_DEFAULT_PAGE,
            size=int(request.args.get("size")) if request.args.get("size") else HISTORICS_DEFAULT_PAGE_SIZE,
            sort_by=request.args.get("sort_by") if request.args.get("sort_by") else HISTORICS_DEFAULT_SORT_FIELD,
            direction=request.args.get("direction") if request.args.get("direction") else HISTORICS_DEFAULT_SORT_DIRECTION,
        )

    @accepts(schema=HistoricSchema, api=api)
    @responds(schema=HistoricSchema, api=api)
    def post(self) -> Historic:
        """Create an historic"""
        return HistoricService.create(request.parsed_obj, commit=True)


@api.route("/<string:version_id>")
class HistoricVersionIdResource(AuthenticatedApi):
    """Historics"""

    @accepts(api=api)
    @responds(schema=HistoricPaginatedSchema)
    def get(self, version_id) -> Pagination:
        """Get historics by version id"""
        return HistoricService.get_by_version_id(
            version_id,
            page=int(request.args.get("page")) if request.args.get("page") else HISTORICS_DEFAULT_PAGE,
            size=int(request.args.get("size")) if request.args.get("size") else HISTORICS_DEFAULT_PAGE_SIZE,
            sort_by=request.args.get("sort_by") if request.args.get("sort_by") else HISTORICS_DEFAULT_SORT_FIELD,
            direction=request.args.get("direction") if request.args.get("direction") else HISTORICS_DEFAULT_SORT_DIRECTION,
        )


@api.route("/<string:historic_id>")
class HistoricIdResource(AuthenticatedApi):
    @responds(api=api)
    def delete(self, historic_id):
        HistoricService.delete_by_id(historic_id=historic_id, commit=True)
        return jsonify(dict(status="Success", id=historic_id))
