from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, Client
from .interface import ClientInterface
from .schema import ClientPaginatedSchema, ClientSchema
from .service import (
    ClientService,
    CLIENTS_DEFAULT_PAGE,
    CLIENTS_DEFAULT_PAGE_SIZE,
    CLIENTS_DEFAULT_SORT_FIELD,
    CLIENTS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import is_manager
from ...common.search import SEARCH_PARAMS


@api.route("/")
class ClientResource(AuthenticatedApi):
    """ Clients """

    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=ClientPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all clients """
        return ClientService.get_all(
            page=int(request.args.get("page", CLIENTS_DEFAULT_PAGE)),
            size=int(request.args.get("size", CLIENTS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", CLIENTS_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", CLIENTS_DEFAULT_SORT_DIRECTION),
        )

    @accepts(schema=ClientSchema, api=api)
    @responds(schema=ClientSchema)
    @requires(is_manager)
    def post(self) -> Client:
        """ Create a client """
        return ClientService.create(request.parsed_obj)


@api.route("/<int:client_id>")
@api.param("clientId", "Client unique ID")
class ClientIdResource(AuthenticatedApi):
    @responds(schema=ClientSchema)
    def get(self, client_id: int) -> Client:
        """ Get single client """

        return ClientService.get_by_id(client_id)

    @requires(is_manager)
    def delete(self, client_id: int) -> Response:
        """Delete single client"""

        id = ClientService.delete_by_id(client_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=ClientSchema, api=api)
    @responds(schema=ClientSchema)
    @requires(is_manager)
    def put(self, client_id: int) -> Client:
        """Update single client"""

        changes: ClientInterface = request.parsed_obj
        db_client = ClientService.get_by_id(client_id)
        return ClientService.update(db_client, changes)
