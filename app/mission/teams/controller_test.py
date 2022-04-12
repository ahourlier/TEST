from unittest.mock import patch

from flask.testing import FlaskClient

from app.auth.users.exceptions import UserNotFoundException
from app.mission import BASE_ROUTE
from app.mission.missions.exceptions import MissionNotFoundException
from app.mission.teams import Team
from app.mission.teams.interface import TeamInterface
from app.mission.teams.schema import TeamPaginatedSchema, TeamSchema
from app.mission.teams.service import (
    TeamService,
    TEAMS_DEFAULT_PAGE,
    TEAMS_DEFAULT_PAGE_SIZE,
    TEAMS_DEFAULT_SORT_FIELD,
    TEAMS_DEFAULT_SORT_DIRECTION,
)
from app.mission.teams.test.fixtures import (
    TEAM_ONE_USER_POSITION,
    TEAM_TWO_USER_POSITION,
)
from app.test.helpers import make_pagination

# FIXTURES IMPORT
from app.test.fixtures import app, client


def make_team(
    id: int = 1,
    user_position: str = TEAM_ONE_USER_POSITION,
    mission_id: int = 1,
    user_id: int = 1,
) -> Team:
    return Team(
        id=id,
        user_position=user_position,
        mission_id=mission_id,
        user_id=user_id,
    )


def get_all_fake_data(**kwargs):
    m1 = make_team(
        123,
        user_position=TEAM_ONE_USER_POSITION,
        mission_id=1,
        user_id=1,
    )
    m2 = make_team(
        456,
        user_position=TEAM_TWO_USER_POSITION,
        mission_id=1,
        user_id=1,
    )

    items = [m1, m2]
    total = 2
    if (
        kwargs.get("term") == "ager"
        or kwargs.get("mission_id") == 2
        or kwargs.get("user_id") == 2
    ):
        items = [m2]
        total = 1
    elif kwargs.get("size") == 1:
        if kwargs.get("page") == 1:
            items = [m1]
        elif kwargs.get("page") == 2:
            items = [m2]
    elif kwargs.get("direction") == "desc" and kwargs.get("sort_by") == "id":
        items = [m2, m1]

    return make_pagination(
        items=items,
        page=kwargs.get("page"),
        per_page=kwargs.get("size"),
        total=total,
    )


def fake_create_team(*args):
    team_interface = args[0]
    if team_interface.get("mission_id") == 1:
        raise MissionNotFoundException
    if team_interface.get("user_id") == 1:
        raise UserNotFoundException
    return make_team(mission_id=2, user_id=2)


def fake_update(team: Team, changes: TeamInterface) -> Team:
    # To fake an update, just return a new object
    updated_team = Team(
        id=team.id,
        user_position=changes["user_position"],
        mission_id=changes["mission_id"],
        user_id=changes["user_id"],
    )
    return updated_team


class TestTeamIdResource:
    @patch.object(TeamService, "get_by_id", lambda id: make_team(id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/teams/123").get_json()
            expected = Team(id=123)
            assert result["id"] == expected.id

    @patch.object(TeamService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/teams/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected
