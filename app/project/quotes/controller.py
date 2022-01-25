from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, Quote
from ..simulations.schema import QuoteSchema, QuotePaginatedSchema
from .interface import QuoteInterface
from .service import (
    QuoteService,
    QUOTES_DEFAULT_PAGE,
    QUOTES_DEFAULT_PAGE_SIZE,
    QUOTES_DEFAULT_SORT_FIELD,
    QUOTES_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import has_project_permission
from ...common.search import SEARCH_PARAMS


@api.route("/")
class QuoteResource(AuthenticatedApi):
    """Quotes"""

    @accepts(*SEARCH_PARAMS, dict(name="project_id", type=int), api=api)
    @responds(schema=QuotePaginatedSchema())
    def get(self) -> Pagination:
        """Get all quotes"""
        return QuoteService.get_all(
            page=int(request.args.get("page", QUOTES_DEFAULT_PAGE)),
            size=int(request.args.get("size", QUOTES_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", QUOTES_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", QUOTES_DEFAULT_SORT_DIRECTION),
            project_id=int(request.args.get("project_id"))
            if request.args.get("project_id") not in [None, ""]
            else None,
        )

    @accepts(schema=QuoteSchema, api=api)
    @responds(schema=QuoteSchema)
    @requires(has_project_permission)
    def post(self) -> Quote:
        """Create a quote"""
        return QuoteService.create(request.parsed_obj)


@api.route("/<int:quote_id>")
@api.param("quoteId", "Quote unique ID")
class QuoteIdResource(AuthenticatedApi):
    @responds(schema=QuoteSchema)
    def get(self, quote_id: int) -> Quote:
        """Get single quote"""

        return QuoteService.get_by_id(quote_id)

    def delete(self, quote_id: int) -> Response:
        """Delete single quote"""

        id = QuoteService.delete_by_id(quote_id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=QuoteSchema, api=api)
    @responds(schema=QuoteSchema)
    @requires(has_project_permission)
    def put(self, quote_id: int) -> Quote:
        """Update single quote"""

        changes: QuoteInterface = request.parsed_obj
        db_quote = QuoteService.get_by_id(quote_id)
        return QuoteService.update(db_quote, changes)
