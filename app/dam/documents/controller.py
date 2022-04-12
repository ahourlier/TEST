from flask_allows import requires

from . import api
from flask import request, Response
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Document
from .interface import DocumentInterface
from .schema import (
    DocumentPaginatedSchema,
    DocumentSchema,
    DocumentGenerateSchema,
    HTMLContentSchema,
    DocumentRequestSchema,
)
from .service import (
    DocumentService,
    DOCUMENTS_DEFAULT_PAGE,
    DOCUMENTS_DEFAULT_PAGE_SIZE,
    DOCUMENTS_DEFAULT_SORT_FIELD,
    DOCUMENTS_DEFAULT_SORT_DIRECTION,
    DocumentGenerationService,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import is_admin, has_project_permission
from ...common.search import SEARCH_PARAMS


@api.route("/")
class DocumentResource(AuthenticatedApi):
    """Documents"""

    @accepts(
        *SEARCH_PARAMS,
        api=api,
    )
    @responds(schema=DocumentPaginatedSchema())
    @requires(is_admin)
    def get(self) -> Pagination:
        """Get all documents"""
        return DocumentService.get_all(
            page=int(request.args.get("page", DOCUMENTS_DEFAULT_PAGE)),
            size=int(request.args.get("size", DOCUMENTS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", DOCUMENTS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", DOCUMENTS_DEFAULT_SORT_DIRECTION
            ),
        )

    @accepts(schema=DocumentGenerateSchema, api=api)
    @responds(schema=DocumentSchema)
    @requires(has_project_permission)
    def post(self) -> Document:
        """Generate a document completed from template"""
        return DocumentService.create(request.parsed_obj)


@api.route("/html/")
class DocumentHTMLResource(AuthenticatedApi):
    @accepts(schema=DocumentRequestSchema, api=api)
    @requires(has_project_permission)
    def post(self) -> Document:
        """Return an HTML text based on a template, completed with corresponding values"""
        return DocumentService.html_document(request.parsed_obj)


@api.route("/<int:document_id>")
@api.param("documentId", "Document unique ID")
class DocumentIdResource(AuthenticatedApi):
    @responds(schema=DocumentSchema(), api=api)
    @requires(is_admin)
    def get(self, document_id: int) -> Document:
        """Get single document"""

        return DocumentService.get_by_id(document_id)

    # TODO To keep until we are sure it's not useful

    # @requires(is_admin)
    # def delete(self, document_id: int) -> Response:
    #     """Delete single document"""
    #     from flask import jsonify
    #
    #     id = DocumentService.delete_by_id(document_id)
    #     return jsonify(dict(status="Success", id=id))
    #
    # @accepts(schema=DocumentSchema(), api=api)
    # @responds(schema=DocumentSchema(), api=api)
    # @requires(is_admin)
    # def put(self, document_id: int) -> Document:
    #     """Update single document"""
    #
    #     changes: DocumentInterface = request.parsed_obj
    #     db_document = DocumentService.get_by_id(document_id)
    #     return DocumentService.update(db_document, changes)
