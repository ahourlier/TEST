from typing import List

from flask import request, Response, jsonify, g

from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from app.common.api import AuthenticatedApi
from app.common.search import SEARCH_PARAMS
from app.project.projects.schema import ProjectPaginatedSchema
from app.project.search import api
from app.project.search.interface import SearchInterface
from app.project.search.model import Search
from app.project.search.schema import (
    SearchSchema,
    SearchRegisterSchema,
    SearchDumpSchema,
    SearchPaginatedSchema,
)
from app.project.search.service import (
    ProjectSearchService,
    ProjectRegisterSearchService,
    SEARCH_DEFAULT_PAGE,
    SEARCH_DEFAULT_PAGE_SIZE,
    SEARCH_DEFAULT_SORT_FIELD,
    SEARCH_DEFAULT_SORT_DIRECTION,
    SAVED_SEARCH_DEFAULT_PAGE,
    SAVED_SEARCH_DEFAULT_PAGE_SIZE,
    SAVED_SEARCH_DEFAULT_SORT_FIELD,
    SAVED_SEARCH_DEFAULT_SORT_DIRECTION,
)


@api.route("/")
class ProjectExecuteSearchResource(AuthenticatedApi):
    """Searchs on projects"""

    @accepts(schema=SearchSchema(), api=api)
    @responds(schema=ProjectPaginatedSchema(), api=api)
    def post(self) -> Pagination:
        """Search on projects"""
        return ProjectSearchService.search_projects(
            request.get_json(),
            page=int(request.args.get("page", SEARCH_DEFAULT_PAGE)),
            size=int(request.args.get("size", SEARCH_DEFAULT_PAGE_SIZE)),
            sort_by=request.args.get("sortBy", SEARCH_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", SEARCH_DEFAULT_SORT_DIRECTION),
        )


@api.route("/save/me/")
class ProjectSearchResource(AuthenticatedApi):
    """Get registered searchs"""

    @responds(schema=SearchDumpSchema(many=True))
    def get(self) -> List[Search]:
        """Get all searchs"""
        return ProjectRegisterSearchService.get_all_raw()

    @accepts(schema=SearchRegisterSchema(), api=api)
    @responds(schema=SearchDumpSchema(), api=api)
    def post(self) -> Search:
        """Create a search"""
        return ProjectRegisterSearchService.create(request.parsed_obj)


@accepts(*SEARCH_PARAMS, api=api)
@api.route("/save_paginated/me")
class PaginatedSearchResource(AuthenticatedApi):
    @responds(schema=SearchPaginatedSchema())
    def get(self) -> Pagination:
        """Get all searchs paginated"""
        return ProjectRegisterSearchService.get_all_paginated(
            page=int(request.args.get("page", SAVED_SEARCH_DEFAULT_PAGE)),
            size=int(request.args.get("size", SAVED_SEARCH_DEFAULT_PAGE_SIZE)),
            sort_by=request.args.get("sortBy", SAVED_SEARCH_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", SAVED_SEARCH_DEFAULT_SORT_DIRECTION
            ),
        )


@api.route("/<int:search_id>/me/")
@api.param("searchId", "Search unique ID")
class SearchIdResource(AuthenticatedApi):
    @responds(schema=SearchDumpSchema(), api=api)
    def get(self, search_id: int) -> Search:
        """Get single search"""
        return ProjectRegisterSearchService.get_by_id(search_id)

    @responds(schema=SearchDumpSchema(many=True))
    def delete(self, search_id: int) -> List[Search]:
        """Delete single search"""

        return ProjectRegisterSearchService.delete_by_id(search_id)

    @accepts(schema=SearchSchema(), api=api)
    @responds(schema=SearchDumpSchema(), api=api)
    def put(self, search_id: int) -> Search:
        """Update single search"""

        changes: SearchInterface = request.parsed_obj
        db_search = ProjectRegisterSearchService.get_by_id(search_id)
        return ProjectRegisterSearchService.update(db_search, changes)
