from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from . import Team
from .model import UserTeamPositions
from ..missions import Mission
from ...auth.users import User

# FIXTURES IMPORT
from app.test.fixtures import app, db

from app.mission.missions.model_test import mission
from app.admin.agencies.model_test import agency
from app.admin.antennas.model_test import antenna, create_antenna_one
from app.admin.clients.model_test import client
from app.auth.users.model_test import user
from .test.fixtures import team


def test_team_create(team: Team):
    assert team


def test_team_retrieve(team: Team, db: SQLAlchemy):
    db.session.add(team)
    db.session.commit()
    s = Team.query.first()
    assert s.__dict__ == team.__dict__


def test_team_update(team: Team, db: SQLAlchemy):
    db.session.add(team)
    db.session.commit()
    team.user_position = "Fake position"
    db.session.add(team)
    db.session.commit()

    res = Team.query.get(team.id)

    assert res.user_position == "Fake position"
    assert res.updated_at is not None
