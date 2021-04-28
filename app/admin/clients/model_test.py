from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.test.fixtures import app, db

from .model import Client

CLIENT_ONE_NAME = "Ville de Nice"
CLIENT_ONE_POSTAL_ADDRESS = "243 Prom. des Anglais, 06200 Nice"
CLIENT_ONE_TITLE = "M."
CLIENT_ONE_LAST_NAME = "MICHEL"
CLIENT_ONE_FIRST_NAME = "Patrick"
CLIENT_ONE_JOB_FUNCTION = "Responsable des rénovations"
CLIENT_ONE_PHONE_NUMBER = {
    "country_code": "FR",
    "national": "01 02 03 04 05",
    "international": "+33 1 02 03 04 05",
}
CLIENT_ONE_EMAIL_ADDRESS = "p.michel@ville-de-nice.fr"
CLIENT_ONE_COMMENT = "N/A"

CLIENT_TWO_NAME = "Quimper'méable"
CLIENT_TWO_POSTAL_ADDRESS = "1 Rue du Roi Gradlon, 29000 Quimper"
CLIENT_TWO_TITLE = "Mme"
CLIENT_TWO_LAST_NAME = "LEGUENNEC"
CLIENT_TWO_FIRST_NAME = "Gwenaëlle"
CLIENT_TWO_JOB_FUNCTION = "Directrice Financière"
CLIENT_TWO_PHONE_NUMBER = {
    "country_code": "FR",
    "national": "01 02 03 04 05",
    "international": "+33 1 02 03 04 05",
}
CLIENT_TWO_EMAIL_ADDRESS = "gl@quimpermeable.bzh"
CLIENT_TWO_COMMENT = "N/A"


def create_client_one() -> Client:
    return Client(
        id=1,
        name=CLIENT_ONE_NAME,
        postal_address=CLIENT_ONE_POSTAL_ADDRESS,
        title=CLIENT_ONE_TITLE,
        last_name=CLIENT_ONE_LAST_NAME,
        first_name=CLIENT_ONE_FIRST_NAME,
        job_function=CLIENT_ONE_JOB_FUNCTION,
        email_address=CLIENT_ONE_EMAIL_ADDRESS,
        comment=CLIENT_ONE_COMMENT,
    )


def create_client_two() -> Client:
    return Client(
        id=2,
        name=CLIENT_TWO_NAME,
        postal_address=CLIENT_TWO_POSTAL_ADDRESS,
        title=CLIENT_TWO_TITLE,
        last_name=CLIENT_TWO_LAST_NAME,
        first_name=CLIENT_TWO_FIRST_NAME,
        job_function=CLIENT_TWO_JOB_FUNCTION,
        email_address=CLIENT_TWO_EMAIL_ADDRESS,
        comment=CLIENT_TWO_COMMENT,
    )


@fixture
def client() -> Client:
    return create_client_one()


def test_client_create(client: Client):
    assert client


def test_client_retrieve(client: Client, db: SQLAlchemy):
    db.session.add(client)
    db.session.commit()
    s = Client.query.first()
    assert s.__dict__ == client.__dict__


def test_client_update(client: Client, db: SQLAlchemy):
    db.session.add(client)
    db.session.commit()
    client.comment = "Rien à signaler"
    db.session.add(client)
    db.session.commit()

    s = Client.query.first()

    assert s.comment == "Rien à signaler"
    assert s.updated_at is not None
