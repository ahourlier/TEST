from flask import request, Response, jsonify, g
from flask_accepts import accepts, responds
from flask_sqlalchemy import Pagination

from . import api, Team
from .interface import TeamInterface
from .schema import TeamPaginatedSchema, TeamSchema, TeamMultipleSchema
from .service import (
    TeamService,
    MISSION_MANAGERS_DEFAULT_PAGE,
    MISSION_MANAGERS_DEFAULT_PAGE_SIZE,
    MISSION_MANAGERS_DEFAULT_SORT_FIELD,
    MISSION_MANAGERS_DEFAULT_SORT_DIRECTION,
)
from ...auth.users.schema import UserPaginatedSchema
from ...common.api import AuthenticatedApi
from ...common.search import SEARCH_PARAMS


@api.route("/")
class TeamResource(AuthenticatedApi):
    """Teams"""

    @accepts(
        *SEARCH_PARAMS,
        dict(name="mission_id", type=int),
        api=api,
    )
    @responds(schema=TeamMultipleSchema())
    def get(self):
        """Get all teams"""
        return TeamService.get_all(
            mission_id=int(request.args.get("mission_id"))
            if request.args.get("mission_id") not in [None, ""]
            else None
        )

    @accepts(schema=TeamMultipleSchema(), api=api)
    @responds(schema=TeamMultipleSchema(), api=api)
    def post(self) -> Response:
        """Create multiple team"""

        return TeamService.create_list(request.parsed_obj, update=False, user=g.user)

    @accepts(schema=TeamMultipleSchema(), api=api)
    @responds(schema=TeamMultipleSchema(), api=api)
    def put(self):
        """Update Multiple team"""

        return TeamService.update_list(request.parsed_obj)


@api.route("/<int:team_id>")
@api.param("teamId", "Team unique ID")
class TeamIdResource(AuthenticatedApi):
    @responds(schema=TeamSchema(), api=api)
    def get(self, team_id: int) -> Team:
        """Get single team"""

        return TeamService.get_by_id(team_id)

    def delete(self, team_id: int) -> Response:
        """Delete single team"""

        id = TeamService.delete_by_id(team_id)
        return jsonify(dict(status="Success", id=id))


@api.route("/managers/")
class MissionManagerResource(AuthenticatedApi):
    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=UserPaginatedSchema())
    def get(self) -> Pagination:
        """Get all managers"""
        return TeamService.get_all_mission_managers(
            page=int(request.args.get("page", MISSION_MANAGERS_DEFAULT_PAGE)),
            size=int(request.args.get("size", MISSION_MANAGERS_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", MISSION_MANAGERS_DEFAULT_SORT_FIELD),
            direction=request.args.get(
                "sortDirection", MISSION_MANAGERS_DEFAULT_SORT_DIRECTION
            ),
        )
