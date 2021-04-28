from typing import List
from unittest.mock import patch
from flask.testing import FlaskClient
from flask_sqlalchemy import Pagination

from app.test.fixtures import client, app
from .model_test import (
    AGENCY_ADDRESS_ONE,
    AGENCY_NAME_ONE,
    AGENCY_NAME_TWO,
    AGENCY_ADDRESS_TWO,
    AGENCY_EMAIL_ONE,
    AGENCY_EMAIL_TWO,
)
from .service import (
    AgencyService,
    AGENCIES_DEFAULT_SORT_FIELD,
    AGENCIES_DEFAULT_SORT_DIRECTION,
    AGENCIES_DEFAULT_PAGE,
    AGENCIES_DEFAULT_PAGE_SIZE,
)
from .schema import AgencySchema, AgencyPaginatedSchema
from .model import Agency
from .interface import AgencyInterface
from .. import BASE_ROUTE
from ...test.helpers import make_pagination


def make_agency(
    id: int = 1,
    name: str = AGENCY_NAME_ONE,
    postal_address: str = AGENCY_ADDRESS_ONE,
    email_address: str = AGENCY_EMAIL_ONE,
) -> Agency:
    return Agency(
        id=id, name=name, postal_address=postal_address, email_address=email_address
    )


def get_all_fake_data(**kwargs):
    a1 = make_agency(
        123,
        name=AGENCY_NAME_ONE,
        postal_address=AGENCY_ADDRESS_ONE,
        email_address=AGENCY_EMAIL_ONE,
    )
    a2 = make_agency(
        456,
        name=AGENCY_NAME_TWO,
        postal_address=AGENCY_ADDRESS_TWO,
        email_address=AGENCY_EMAIL_TWO,
    )

    items = [a1, a2]
    total = 2
    if kwargs.get("term") == "ari":
        items = [a2]
        total = 1
    elif kwargs.get("size") == 1:
        if kwargs.get("page") == 1:
            items = [a1]
        elif kwargs.get("page") == 2:
            items = [a2]
    elif kwargs.get("direction") == "asc" and kwargs.get("sort_by") == "name":
        items = [a2, a1]

    return make_pagination(
        items=items, page=kwargs.get("page"), per_page=kwargs.get("size"), total=total,
    )


class TestAgencyResource:
    @patch.object(
        AgencyService, "get_all", get_all_fake_data,
    )
    def test_get(self, client: FlaskClient):
        with client:
            # Test with no query parameters
            results = client.get(
                f"/api/{BASE_ROUTE}/agencies/", follow_redirects=True
            ).get_json()
            expected = AgencyPaginatedSchema().dump(
                get_all_fake_data(
                    page=AGENCIES_DEFAULT_PAGE,
                    size=AGENCIES_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=AGENCIES_DEFAULT_SORT_FIELD,
                    direction=AGENCIES_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Change size
            results = client.get(
                f"/api/{BASE_ROUTE}/agencies/",
                query_string=dict(size=1),
                follow_redirects=True,
            ).get_json()
            expected = AgencyPaginatedSchema().dump(
                get_all_fake_data(
                    page=AGENCIES_DEFAULT_PAGE,
                    size=1,
                    term=None,
                    sort_by=AGENCIES_DEFAULT_SORT_FIELD,
                    direction=AGENCIES_DEFAULT_SORT_DIRECTION,
                )
            )

            assert results == expected

            # Change page
            results = client.get(
                f"/api/{BASE_ROUTE}/agencies/",
                query_string=dict(page=2, size=1),
                follow_redirects=True,
            ).get_json()
            expected = AgencyPaginatedSchema().dump(
                get_all_fake_data(
                    page=2,
                    size=1,
                    term=None,
                    sort_by=AGENCIES_DEFAULT_SORT_FIELD,
                    direction=AGENCIES_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Search
            results = client.get(
                f"/api/{BASE_ROUTE}/agencies/",
                query_string=dict(term="ari"),
                follow_redirects=True,
            ).get_json()
            expected = AgencyPaginatedSchema().dump(
                get_all_fake_data(
                    page=AGENCIES_DEFAULT_PAGE,
                    size=AGENCIES_DEFAULT_PAGE_SIZE,
                    term="ari",
                    sort_by=AGENCIES_DEFAULT_SORT_FIELD,
                    direction=AGENCIES_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Sort
            results = client.get(
                f"/api/{BASE_ROUTE}/agencies/",
                query_string=dict(sortBy="name", sortDirection="asc"),
                follow_redirects=True,
            ).get_json()
            expected = AgencyPaginatedSchema().dump(
                get_all_fake_data(
                    page=AGENCIES_DEFAULT_PAGE,
                    size=AGENCIES_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by="name",
                    direction="asc",
                )
            )
            assert results == expected

    @patch.object(
        AgencyService, "create", lambda create_request: Agency(**create_request)
    )
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(
                name=AGENCY_NAME_ONE,
                postal_address=AGENCY_ADDRESS_ONE,
                email_address=AGENCY_EMAIL_ONE,
            )
            result = client.post(
                f"/api/{BASE_ROUTE}/agencies/", json=payload
            ).get_json()
            expected = AgencySchema().dump(
                Agency(
                    name=payload["name"],
                    postal_address=payload["postal_address"],
                    email_address=payload["email_address"],
                )
            )
            assert result == expected


def fake_update(agency: Agency, changes: AgencyInterface) -> Agency:
    # To fake an update, just return a new object
    updated_agency = Agency(
        id=agency.id,
        name=changes["name"],
        postal_address=changes["postal_address"],
        email_address=changes["email_address"],
    )
    return updated_agency


class TestAgencyIdResource:
    @patch.object(AgencyService, "get_by_id", lambda id: make_agency(id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/agencies/123").get_json()
            expected = Agency(id=123)
            assert result["id"] == expected.id

    @patch.object(AgencyService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/agencies/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(AgencyService, "get_by_id", lambda id: make_agency(id=id))
    @patch.object(AgencyService, "update", fake_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/agencies/123",
                json={
                    "name": AGENCY_NAME_ONE,
                    "postal_address": AGENCY_ADDRESS_ONE,
                    "email_address": AGENCY_EMAIL_ONE,
                },
            ).get_json()
            expected = AgencySchema().dump(
                Agency(
                    id=123,
                    name=AGENCY_NAME_ONE,
                    postal_address=AGENCY_ADDRESS_ONE,
                    email_address=AGENCY_EMAIL_ONE,
                )
            )
            assert result == expected
