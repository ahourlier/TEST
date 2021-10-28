from typing import List

from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires

# from flask_sqlalchemy import Pagination

from app.common.api import AuthenticatedApi
from app.common.permissions import is_manager
from . import api
from .interface import ReferentInterface
from .model import Referent

# from .schema import ReferentPaginatedSchema, ReferentSchema
from .schema import ReferentSchema
from .service import (
    ReferentService,
    # CLIENTS_DEFAULT_PAGE,
    # CLIENTS_DEFAULT_PAGE_SIZE,
    # CLIENTS_DEFAULT_SORT_FIELD,
    # CLIENTS_DEFAULT_SORT_DIRECTION,
)

# from ...common.permissions import is_manager
# from ...common.search import SEARCH_PARAMS


@api.route("/")
class ReferentResource(AuthenticatedApi):
    """ Referents """

    # @responds(schema=ReferentSchema)
    def get(self):
        """ Get all referents """
        return ReferentService.get_all()

    @accepts(schema=ReferentSchema, api=api)
    @responds(schema=ReferentSchema)
    @requires(is_manager)
    def post(self) -> Referent:
        """ Create a referent """
        return ReferentService.create(request.parsed_obj)


@api.route("/<int:referent_id>")
@api.param("referentId", "Referent unique ID")
class ReferentIdResource(AuthenticatedApi):
    @responds(schema=ReferentSchema)
    def get(self, referent_id: int) -> Referent:
        """ Get single referent """

        return ReferentService.get_by_id(referent_id)

    @requires(is_manager)
    def delete(self, referent_id: int) -> Response:
        """Delete single referent"""

        id = ReferentService.delete_by_id(referent_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=ReferentSchema, api=api)
    @responds(schema=ReferentSchema)
    @requires(is_manager)
    def put(self, referent_id: int) -> Referent:
        """Update single referent"""

        changes: ReferentInterface = request.parsed_obj
        db_referent = ReferentService.get_by_id(referent_id)
        return ReferentService.update(db_referent, changes)
