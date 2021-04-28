from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.test.fixtures import app, db
from ..agencies.model_test import agency

from ..agencies.model import Agency
from .model import Antenna


ANTENNA_NAME_ONE = "Toulouse"
ANTENNA_ADDRESS_ONE = "Au milieu"
ANTENNA_EMAIL_ONE = "toulouse-antenna@email.com"

ANTENNA_NAME_TWO = "Paris"
ANTENNA_ADDRESS_TWO = "Rue Godot de Mauroy"
ANTENNA_EMAIL_TWO = "paris-antenna@email.com"


def create_antenna_one(agency_id) -> Antenna:
    return Antenna(
        name=ANTENNA_NAME_ONE,
        postal_address=ANTENNA_ADDRESS_ONE,
        email_address=ANTENNA_EMAIL_ONE,
        agency_id=agency_id,
    )


def create_antenna_two(agency_id) -> Antenna:
    return Antenna(
        name=ANTENNA_NAME_TWO,
        postal_address=ANTENNA_ADDRESS_TWO,
        email_address=ANTENNA_EMAIL_TWO,
        agency_id=agency_id,
    )


@fixture
def antenna(agency: Agency, db: SQLAlchemy) -> Antenna:
    db.session.add(agency)
    db.session.commit()
    return create_antenna_one(agency_id=agency.id)


def test_antenna_create(antenna: Antenna):
    assert antenna


def test_antenna_retrieve(antenna: Antenna, db: SQLAlchemy):
    db.session.add(antenna)
    db.session.commit()
    s = Antenna.query.first()
    assert s.__dict__ == antenna.__dict__


def test_antenna_update(antenna: Antenna, db: SQLAlchemy):
    db.session.add(antenna)
    db.session.commit()
    antenna.name = "My new antenna"
    db.session.add(antenna)
    db.session.commit()

    res = Antenna.query.get(antenna.id)

    assert res.name == "My new antenna"
    assert res.updated_at is not None
