from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.admin.agencies import Agency
from app.admin.agencies.model_test import create_agency_one, create_agency_two


@fixture
def agency_one(db: SQLAlchemy) -> Agency:
    a1: Agency = create_agency_one()
    db.session.add(a1)
    db.session.commit()
    return a1


@fixture
def agency_two(db: SQLAlchemy) -> Agency:
    a2: Agency = create_agency_two()
    db.session.add(a2)
    db.session.commit()
    return a2
