from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, CommentSchema, Comment
from .interface import CommentInterface
from .schema import CommentPaginatedSchema
from .service import (
    CommentService,
    COMMENTS_DEFAULT_PAGE,
    COMMENTS_DEFAULT_PAGE_SIZE,
    COMMENTS_DEFAULT_SORT_FIELD,
    COMMENTS_DEFAULT_SORT_DIRECTION,
)
from ...common.api import AuthenticatedApi
from ...common.permissions import has_project_permission
from ...common.search import SEARCH_PARAMS


@api.route("/")
class CommentResource(AuthenticatedApi):
    """ Comments """

    # TODO endpoint_access_check
    @accepts(
        *SEARCH_PARAMS,
        dict(name="author_id", type=int),
        dict(name="project_id", type=int),
        api=api,
    )
    @responds(schema=CommentPaginatedSchema())
    def get(self) -> Pagination:
        """ Get all comments """
        return CommentService.get_all(
            page=int(request.args.get("page", COMMENTS_DEFAULT_PAGE)),
            size=int(request.args.get("size", COMMENTS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", COMMENTS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", COMMENTS_DEFAULT_SORT_DIRECTION
            ),
            project_id=int(request.args.get("project_id"))
            if request.args.get("project_id") not in [None, ""]
            else None,
            author_id=int(request.args.get("author_id"))
            if request.args.get("author_id") not in [None, ""]
            else None,
        )

    @accepts(schema=CommentSchema())
    @responds(schema=CommentPaginatedSchema())
    @requires(has_project_permission)
    def post(self) -> Pagination:
        """ Create an comment """
        return CommentService.create(request.parsed_obj)


@api.route("/<int:comment_id>")
@api.param("commentId", "Comment unique ID")
class CommentIdResource(AuthenticatedApi):
    # TODO endpoint_access_check
    @responds(schema=CommentSchema)
    def get(self, comment_id: int) -> Comment:
        """ Get single comment """

        return CommentService.get_by_id(comment_id)

    # TODO endpoint_access_check
    @responds(schema=CommentPaginatedSchema())
    def delete(self, comment_id: int) -> Pagination:
        """Delete single comment"""
        return CommentService.delete_by_id(comment_id)

    @accepts(schema=CommentSchema, api=api)
    @responds(schema=CommentPaginatedSchema())
    @requires(has_project_permission)
    def put(self, comment_id: int) -> Pagination:
        """Update single comment"""

        changes: CommentInterface = request.parsed_obj
        db_comment = CommentService.get_by_id(comment_id)
        return CommentService.update(db_comment, changes)
