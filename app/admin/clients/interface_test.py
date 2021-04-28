from pytest import fixture

from app.admin.clients import Client
from app.admin.clients.interface import ClientInterface
from app.admin.clients.model_test import (
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


def get_client_one_interface() -> ClientInterface:
    return ClientInterface(
        name=CLIENT_ONE_NAME,
        postal_address=CLIENT_ONE_POSTAL_ADDRESS,
        title=CLIENT_ONE_TITLE,
        last_name=CLIENT_ONE_LAST_NAME,
        first_name=CLIENT_ONE_FIRST_NAME,
        job_function=CLIENT_ONE_JOB_FUNCTION,
        email_address=CLIENT_ONE_EMAIL_ADDRESS,
        comment=CLIENT_ONE_COMMENT,
    )


@fixture
def interface() -> ClientInterface:
    return get_client_one_interface()


def test_client_interface_create(interface: ClientInterface):
    assert interface


def test_client_interface_ok(interface: ClientInterface):
    client = Client(**interface)
    assert client
