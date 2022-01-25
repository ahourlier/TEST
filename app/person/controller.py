from flask_accepts import accepts, responds
from flask import request, Response, jsonify
from flask_allows import requires
from flask_sqlalchemy import Pagination

from . import api, Person
from .schema import PersonSchema, PersonPaginatedSchema
from .service import (
    PersonService,
    PERSON_DEFAULT_PAGE,
    PERSON_DEFAULT_PAGE_SIZE,
    PERSON_DEFAULT_SORT_FIELD,
    PERSON_DEFAULT_SORT_DIRECTION,
)
from ..common.api import AuthenticatedApi
from ..common.permissions import is_manager

SEARCH_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="antennaId", type=int),
]


@api.route("")
class PersonResource(AuthenticatedApi):
    """Person"""

    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=PersonPaginatedSchema())
    def get(self) -> Pagination:
        """Get all clients"""
        return PersonService.get_all(
            page=int(request.args.get("page", PERSON_DEFAULT_PAGE)),
            size=int(request.args.get("size", PERSON_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", PERSON_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", PERSON_DEFAULT_SORT_DIRECTION),
            antenna_id=request.args.get("antennaId")
            if request.args.get("antennaId") not in [None, ""]
            else None,
        )

    @accepts(schema=PersonSchema, api=api)
    @responds(schema=PersonSchema)
    # @requires(is_manager)
    def post(self) -> Person:
        """Create a client"""
        return PersonService.create(request.parsed_obj)


@api.route("/<int:person_id>")
@api.param("PersonId", "Person unique id")
class PersonIdResource(AuthenticatedApi):
    """Person id resource"""

    @responds(schema=PersonSchema())
    def get(self, person_id: int):
        """Get one person"""
        return PersonService.get(person_id)

    @accepts(schema=PersonSchema, api=api)
    @responds(schema=PersonSchema)
    # @requires(is_manager)
    def put(self, person_id: int) -> Person:
        """Update a person"""
        db_person = PersonService.get(person_id)
        return PersonService.update(db_person, request.parsed_obj)

    # @requires(is_manager)
    def delete(self, person_id: int) -> Response:
        """Update a person"""
        id = PersonService.delete(person_id)
        return jsonify(dict(status="Success", id=id))
