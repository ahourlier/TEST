from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.admin.agencies import Agency
from app.admin.antennas import Antenna
from app.admin.antennas.model_test import create_antenna_one, create_antenna_two
from app.admin.agencies.test.fixtures import agency_one, agency_two


@fixture
def antenna_one(db: SQLAlchemy, agency_one: Agency) -> Antenna:
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)
    db.session.commit()
    return a1


@fixture
def antenna_two(db: SQLAlchemy, agency_two: Agency) -> Antenna:
    a2: Antenna = create_antenna_two(agency_two.id)
    db.session.add(a2)
    db.session.commit()
    return a2
