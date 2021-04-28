from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.admin.clients import Client
from app.admin.clients.model_test import create_client_one, create_client_two


@fixture
def client_one(db: SQLAlchemy) -> Client:
    c1: Client = create_client_one()
    db.session.add(c1)
    db.session.commit()
    return c1


@fixture
def client_two(db: SQLAlchemy) -> Client:
    c2: Client = create_client_two()
    db.session.add(c2)
    db.session.commit()
    return c2
