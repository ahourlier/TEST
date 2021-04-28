from flask_sqlalchemy import SQLAlchemy
from pytest import fixture
import datetime

from app.mission.missions.model import Mission, MissionStatus


# FIXTURES IMPORT
from app.test.fixtures import app, db
from .test.fixtures import mission
from app.admin.agencies.model_test import agency
from app.admin.antennas.model_test import antenna, create_antenna_one
from app.admin.clients.model_test import client


def test_mission_create(mission: Mission):
    assert mission


def test_mission_retrieve(mission: Mission, db: SQLAlchemy):
    db.session.add(mission)
    db.session.commit()
    s = Mission.query.first()
    assert s.__dict__ == mission.__dict__


def test_mission_update(mission: Mission, db: SQLAlchemy):
    db.session.add(mission)
    db.session.commit()
    mission.name = "Mission reborn"
    db.session.add(mission)
    db.session.commit()

    res = Mission.query.get(mission.id)

    assert res.name == "Mission reborn"
    assert res.updated_at is not None
