from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.auth.users import User
from app.mission.missions import Mission
from app.mission.teams import Team
from app.mission.teams.model import UserTeamPositions

# FIXTURES IMPORT
from app.test.fixtures import app, db
from app.mission.missions.test.fixtures import mission, mission_one
from app.admin.agencies.model_test import agency
from app.admin.antennas.model_test import antenna, create_antenna_one
from app.auth.users.model_test import user

TEAM_ONE_USER_POSITION = UserTeamPositions.COLLABORATOR
TEAM_TWO_USER_POSITION = UserTeamPositions.MISSION_MANAGER


def create_team_one(mission_id, user_id) -> Team:
    return Team(
        user_position=TEAM_ONE_USER_POSITION, mission_id=mission_id, user_id=user_id,
    )


def create_team_two(mission_id, user_id) -> Team:
    return Team(
        user_position=TEAM_TWO_USER_POSITION, mission_id=mission_id, user_id=user_id,
    )


@fixture
def team(mission: Mission, user: User, db: SQLAlchemy) -> Team:
    db.session.add(mission)
    db.session.add(user)
    db.session.commit()
    return create_team_one(mission_id=mission.id, user_id=user.id)


@fixture
def team_one(mission_one: Mission, user: User, db: SQLAlchemy) -> Team:
    t1: Team = create_team_one(mission_id=mission_one.id, user_id=user.id)
    db.session.add(t1)
    db.session.commit()
    return t1


@fixture
def team_two(mission_one: Mission, user: User, db: SQLAlchemy) -> Team:
    t2: Team = create_team_two(mission_id=mission_one.id, user_id=user.id)
    db.session.add(t2)
    db.session.commit()
    return t2
