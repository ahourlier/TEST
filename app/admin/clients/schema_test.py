from pytest import fixture

from .model import Client
from .model_test import (
    CLIENT_ONE_NAME,
    CLIENT_ONE_POSTAL_ADDRESS,
    CLIENT_ONE_TITLE,
    CLIENT_ONE_LAST_NAME,
    CLIENT_ONE_FIRST_NAME,
    CLIENT_ONE_JOB_FUNCTION,
    CLIENT_ONE_PHONE_NUMBER,
    CLIENT_ONE_EMAIL_ADDRESS,
    CLIENT_ONE_COMMENT,
)
from .schema import ClientSchema


@fixture
def schema() -> ClientSchema:
    return ClientSchema()


def test_client_schema_create(schema: ClientSchema):
    assert schema


def test_client_schema_ok(schema: ClientSchema):
    params = schema.load(
        {
            "name": CLIENT_ONE_NAME,
            "postal_address": CLIENT_ONE_POSTAL_ADDRESS,
            "title": CLIENT_ONE_TITLE,
            "last_name": CLIENT_ONE_LAST_NAME,
            "first_name": CLIENT_ONE_FIRST_NAME,
            "job_function": CLIENT_ONE_JOB_FUNCTION,
            "email_address": CLIENT_ONE_EMAIL_ADDRESS,
            "comment": CLIENT_ONE_COMMENT,
        }
    )

    client = Client(**params)

    assert client.name == CLIENT_ONE_NAME
    assert client.postal_address == CLIENT_ONE_POSTAL_ADDRESS
    assert client.title == CLIENT_ONE_TITLE
    assert client.last_name == CLIENT_ONE_LAST_NAME
    assert client.first_name == CLIENT_ONE_FIRST_NAME
    assert client.job_function == CLIENT_ONE_JOB_FUNCTION
    assert client.email_address == CLIENT_ONE_EMAIL_ADDRESS
    assert client.comment == CLIENT_ONE_COMMENT
