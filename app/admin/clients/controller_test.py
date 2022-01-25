from typing import List
from unittest.mock import patch
from flask.testing import FlaskClient
from flask_sqlalchemy import Pagination

from app.test.fixtures import client as test_client, app
from .interface import ClientInterface
from .interface_test import get_client_one_interface
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
    create_client_one,
    create_client_two,
    CLIENT_TWO_NAME,
)
from .service import (
    ClientService,
    CLIENTS_DEFAULT_SORT_FIELD,
    CLIENTS_DEFAULT_SORT_DIRECTION,
    CLIENTS_DEFAULT_PAGE,
    CLIENTS_DEFAULT_PAGE_SIZE,
)
from .schema import ClientSchema, ClientPaginatedSchema
from .model import Client
from .. import BASE_ROUTE
from ...test.helpers import make_pagination


def make_client(
    id: int = 1,
    name: str = CLIENT_ONE_NAME,
    postal_address: str = CLIENT_ONE_POSTAL_ADDRESS,
    title: str = CLIENT_ONE_TITLE,
    last_name: str = CLIENT_ONE_LAST_NAME,
    first_name: str = CLIENT_ONE_FIRST_NAME,
    job_function: str = CLIENT_ONE_JOB_FUNCTION,
    phone_number: str = CLIENT_ONE_PHONE_NUMBER,
    email_address: str = CLIENT_ONE_EMAIL_ADDRESS,
    comment: str = CLIENT_ONE_COMMENT,
) -> Client:
    return Client(
        id=id,
        name=name,
        postal_address=postal_address,
        title=title,
        last_name=last_name,
        first_name=first_name,
        job_function=job_function,
        email_address=email_address,
        comment=comment,
    )


def get_all_fake_data(**kwargs):
    c1 = create_client_one()
    c2 = create_client_two()

    items = [c1, c2]
    total = 2
    if kwargs.get("term") == "naël":
        items = [c2]
        total = 1
    elif kwargs.get("size") == 1:
        if kwargs.get("page") == 1:
            items = [c1]
        elif kwargs.get("page") == 2:
            items = [c2]
    elif kwargs.get("direction") == "asc" and kwargs.get("sort_by") == "name":
        items = [c2, c1]

    return make_pagination(
        items=items,
        page=kwargs.get("page"),
        per_page=kwargs.get("size"),
        total=total,
    )


class TestClientResource:
    @patch.object(
        ClientService,
        "get_all",
        get_all_fake_data,
    )
    def test_get(self, test_client: FlaskClient):
        with test_client:
            # Test with no query parameters
            results = test_client.get(
                f"/api/{BASE_ROUTE}/clients/", follow_redirects=True
            ).get_json()
            expected = ClientPaginatedSchema().dump(
                get_all_fake_data(
                    page=CLIENTS_DEFAULT_PAGE,
                    size=CLIENTS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=CLIENTS_DEFAULT_SORT_FIELD,
                    direction=CLIENTS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Change size
            results = test_client.get(
                f"/api/{BASE_ROUTE}/clients/",
                query_string=dict(size=1),
                follow_redirects=True,
            ).get_json()
            expected = ClientPaginatedSchema().dump(
                get_all_fake_data(
                    page=CLIENTS_DEFAULT_PAGE,
                    size=1,
                    term=None,
                    sort_by=CLIENTS_DEFAULT_SORT_FIELD,
                    direction=CLIENTS_DEFAULT_SORT_DIRECTION,
                )
            )

            assert results == expected

            # Change page
            results = test_client.get(
                f"/api/{BASE_ROUTE}/clients/",
                query_string=dict(page=2, size=1),
                follow_redirects=True,
            ).get_json()
            expected = ClientPaginatedSchema().dump(
                get_all_fake_data(
                    page=2,
                    size=1,
                    term=None,
                    sort_by=CLIENTS_DEFAULT_SORT_FIELD,
                    direction=CLIENTS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Search
            results = test_client.get(
                f"/api/{BASE_ROUTE}/clients/",
                query_string=dict(term="naël"),
                follow_redirects=True,
            ).get_json()
            expected = ClientPaginatedSchema().dump(
                get_all_fake_data(
                    page=CLIENTS_DEFAULT_PAGE,
                    size=CLIENTS_DEFAULT_PAGE_SIZE,
                    term="naël",
                    sort_by=CLIENTS_DEFAULT_SORT_FIELD,
                    direction=CLIENTS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Sort
            results = test_client.get(
                f"/api/{BASE_ROUTE}/clients/",
                query_string=dict(sortBy="name", sortDirection="asc"),
                follow_redirects=True,
            ).get_json()
            expected = ClientPaginatedSchema().dump(
                get_all_fake_data(
                    page=CLIENTS_DEFAULT_PAGE,
                    size=CLIENTS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by="name",
                    direction="asc",
                )
            )
            assert results == expected

    @patch.object(
        ClientService, "create", lambda create_request: Client(**create_request)
    )
    def test_post(self, test_client: FlaskClient):
        with test_client:
            payload = get_client_one_interface()
            result = test_client.post(
                f"/api/{BASE_ROUTE}/clients/", json=payload
            ).get_json()
            expected = ClientSchema().dump(Client(**payload))
            assert result == expected


def fake_update(client: Client, changes: ClientInterface) -> Client:
    client.name = changes["name"]
    return client


class TestClientIdResource:
    @patch.object(ClientService, "get_by_id", lambda id: make_client(id=id))
    def test_get(self, test_client: FlaskClient):
        with test_client:
            result = test_client.get(f"/api/{BASE_ROUTE}/clients/123").get_json()
            expected = Client(id=123)
            assert result["id"] == expected.id

    @patch.object(ClientService, "delete_by_id", lambda id: id)
    def test_delete(self, test_client: FlaskClient):
        with test_client:
            result = test_client.delete(f"/api/{BASE_ROUTE}/clients/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(ClientService, "get_by_id", lambda id: make_client(id=id))
    @patch.object(ClientService, "update", fake_update)
    def test_put(self, test_client: FlaskClient):
        with test_client:
            result = test_client.put(
                f"/api/{BASE_ROUTE}/clients/1",
                json={"name": CLIENT_TWO_NAME},
            ).get_json()

            initial_client = create_client_one()
            initial_client.name = CLIENT_TWO_NAME

            expected = ClientSchema().dump(initial_client)
            assert result == expected
