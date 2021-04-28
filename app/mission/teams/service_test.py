from typing import List

import pytest
from flask_sqlalchemy import SQLAlchemy, Pagination

from app.mission.teams import Team
from .error_handlers import TeamNotFoundException
from .interface import TeamInterface
from .interface_test import get_team_one_interface
from .service import TeamService

from ..missions import Mission
from ..missions.exceptions import MissionNotFoundException
from ..missions.interface import MissionInterface
from ...admin.agencies import Agency
from ...auth.users import User
from ...auth.users.exceptions import UserNotFoundException

# FIXTURES IMPORT
from app.test.fixtures import app, db
from app.mission.missions.test.fixtures import mission, mission_one, mission_two
from app.admin.agencies.model_test import agency
from app.admin.antennas.model_test import antenna, create_antenna_one
from app.admin.clients.model_test import client
from app.auth.users.model_test import user
from app.auth.users.service_test import user_one, user_two
from .test.fixtures import team_one, team_two, TEAM_ONE_USER_POSITION
from ...common.exceptions import InconsistentUpdateIdException


def test_get_by_id(team_one: Team):
    db_team = TeamService.get_by_id(1)
    assert db_team == team_one

    with pytest.raises(TeamNotFoundException) as excinfo:
        TeamService.get_by_id(42)
    assert excinfo.type == TeamNotFoundException


def test_update_inconsistent_id(team_one: Team):
    inconsistent_change: TeamInterface = TeamInterface(id=42)
    with pytest.raises(InconsistentUpdateIdException) as excinfo:
        TeamService.update(team_one, inconsistent_change)
    assert excinfo.type == InconsistentUpdateIdException


def test_update_change_mission(team_one: Team, mission_two: Mission):
    change_mission: TeamInterface = TeamInterface(mission_id=mission_two.id)
    TeamService.update(team_one, change_mission)
    result: Team = Team.query.get(1)
    assert result.mission == mission_two
    assert mission_two.teams[0] == result


def test_update_change_user(team_one: Team, user_two: User):
    change_user: TeamInterface = TeamInterface(user_id=user_two.id)
    TeamService.update(team_one, change_user)
    result: Team = Team.query.get(1)
    assert result.user == user_two
    assert user_two.teams[0] == result


def test_has_changed(team_one: Team):
    changes: TeamInterface = TeamInterface(user_position=team_one.user_position)
    assert TeamService.has_changed(team_one, changes) is False

    changes_2: TeamInterface = TeamInterface(user_position="covfefe")
    assert TeamService.has_changed(team_one, changes_2) is True


def test_delete_by_id(
    team_one: Team,
    team_two: Team,
    mission_one: Mission,
    user_one: User,
    db: SQLAlchemy,
):

    deleted_id = TeamService.delete_by_id(1)
    db.session.commit()

    with pytest.raises(TeamNotFoundException) as excinfo:
        TeamService.delete_by_id(42)
    assert excinfo.type == TeamNotFoundException

    results: List[Team] = Team.query.all()

    assert mission_one.teams == [team_two]
    assert user_one.teams == [team_two]
    assert len(results) == 1
    assert team_one not in results and team_two in results
    assert deleted_id == 1
