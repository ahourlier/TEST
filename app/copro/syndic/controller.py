import os

from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination
from . import api
from .model import Syndic
from .schema import (
    SyndicPaginatedSchema,
    SyndicCreateSchema,
    SyndicSchema,
    SyndicUpdateSchema,
)
from .service import SyndicService
from ... import db
from ...common.api import AuthenticatedApi
from ...common.permissions import (
    is_manager,
    is_contributor,
    is_admin,
    filter_response_with_clients_access,
    has_mission_permission,
)
from ...common.search import SEARCH_PARAMS
import app.mission.permissions as missions_permissions
from ...common.tasks import create_task


@api.route("")
class SyndicResource(AuthenticatedApi):
    """Syndic"""

    @accepts(schema=SyndicCreateSchema(), api=api)
    @responds(schema=SyndicSchema(), api=api)
    def post(self) -> Syndic:
        """Create a syndic"""
        return SyndicService.create(request.parsed_obj)


@api.route("/<int:syndic_id>")
@api.param("syndicId", "Syndic unique ID")
class SyndicIdResource(AuthenticatedApi):
    @responds(schema=SyndicSchema(), api=api)
    @accepts(schema=SyndicUpdateSchema(), api=api)
    @requires(is_contributor)
    def put(self, syndic_id: int):
        db_syndic = SyndicService.get(syndic_id)
        return SyndicService.update(db_syndic, request.parsed_obj, syndic_id)

    @requires(is_contributor)
    def delete(self, syndic_id: int):
        SyndicService.delete(syndic_id)
        return jsonify(dict(status="Success", id=syndic_id))
