from flask import request
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Historic, HistoricSchema
from .schema import HistoricPaginatedSchema
from .service import (
    HistoricService
)
from app.common.api import AuthenticatedApi


@api.route("/")
class HistoricResource(AuthenticatedApi):
    """Historics"""

    @accepts(api=api)
    @responds(schema=HistoricPaginatedSchema)
    def get(self) -> Pagination:
        """Get all historics"""
        return HistoricService.get_all()

    @accepts(schema=HistoricSchema, api=api)
    @responds(schema=HistoricSchema, api=api)
    def post(self) -> Historic:
        """Create an historic"""

        return HistoricService.create(request.parsed_obj, commit=True)