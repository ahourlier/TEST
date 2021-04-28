from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.test.fixtures import app, db

from .model import Agency

AGENCY_NAME_ONE = "Toulouse"
AGENCY_ADDRESS_ONE = "Place Saint-Pierre"
AGENCY_EMAIL_ONE = "toulouse-agency@email.com"

AGENCY_NAME_TWO = "Paris"
AGENCY_ADDRESS_TWO = "Strasbourg.St.denis"
AGENCY_EMAIL_TWO = "paris-agency@email.com"


def create_agency_one() -> Agency:
    return Agency(
        name=AGENCY_NAME_ONE,
        postal_address=AGENCY_ADDRESS_ONE,
        email_address=AGENCY_EMAIL_ONE,
    )


def create_agency_two() -> Agency:
    return Agency(
        name=AGENCY_NAME_TWO,
        postal_address=AGENCY_ADDRESS_TWO,
        email_address=AGENCY_EMAIL_TWO,
    )


@fixture
def agency() -> Agency:
    return create_agency_one()


def test_agency_create(agency: Agency):
    assert agency


def test_agency_retrieve(agency: Agency, db: SQLAlchemy):
    db.session.add(agency)
    db.session.commit()
    s = Agency.query.first()
    assert s.__dict__ == agency.__dict__


def test_agency_update(agency: Agency, db: SQLAlchemy):
    db.session.add(agency)
    db.session.commit()
    agency.name = "Tourcoing-sur-Marnes"
    db.session.add(agency)
    db.session.commit()

    assert agency.name == "Tourcoing-sur-Marnes"
    assert agency.updated_at is not None
