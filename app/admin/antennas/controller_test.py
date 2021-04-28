from unittest.mock import patch

from flask.testing import FlaskClient

from app.admin import BASE_ROUTE
from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.antennas import Antenna, AntennaSchema
from app.admin.antennas.interface import AntennaInterface
from app.admin.antennas.model_test import (
    ANTENNA_NAME_ONE,
    ANTENNA_ADDRESS_ONE,
    ANTENNA_EMAIL_ONE,
    ANTENNA_NAME_TWO,
    ANTENNA_ADDRESS_TWO,
    ANTENNA_EMAIL_TWO,
)
from app.admin.antennas.schema import AntennaPaginatedSchema
from app.admin.antennas.service import (
    AntennaService,
    ANTENNAS_DEFAULT_PAGE,
    ANTENNAS_DEFAULT_PAGE_SIZE,
    ANTENNAS_DEFAULT_SORT_FIELD,
    ANTENNAS_DEFAULT_SORT_DIRECTION,
)
from app.test.helpers import make_pagination
from app.test.fixtures import app, client


def make_antenna(
    id: int = 1,
    name: str = ANTENNA_NAME_ONE,
    postal_address: str = ANTENNA_ADDRESS_ONE,
    email_address: str = ANTENNA_EMAIL_ONE,
    agency_id: int = 1,
) -> Antenna:
    return Antenna(
        id=id,
        name=name,
        postal_address=postal_address,
        email_address=email_address,
        agency_id=agency_id,
    )


def get_all_fake_data(**kwargs):
    a1 = make_antenna(
        123,
        name=ANTENNA_NAME_ONE,
        postal_address=ANTENNA_ADDRESS_ONE,
        email_address=ANTENNA_EMAIL_ONE,
        agency_id=1,
    )
    a2 = make_antenna(
        456,
        name=ANTENNA_NAME_TWO,
        postal_address=ANTENNA_ADDRESS_TWO,
        email_address=ANTENNA_EMAIL_TWO,
        agency_id=2,
    )

    items = [a1, a2]
    total = 2
    if kwargs.get("term") == "ari" or kwargs.get("agency_id") == 2:
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


def fake_create_antenna(*args):
    antenna_interface = args[0]
    if antenna_interface.get("agency_id") == 1:
        raise AgencyNotFoundException()
    return make_antenna(agency_id=2)


class TestAntennaResource:
    @patch.object(AntennaService, "get_all", get_all_fake_data)
    def test_get(self, client: FlaskClient):
        with client:
            # Test with no query parameters
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/", follow_redirects=True
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=ANTENNAS_DEFAULT_PAGE,
                    size=ANTENNAS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
                    direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Change size
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/",
                query_string=dict(size=1),
                follow_redirects=True,
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=ANTENNAS_DEFAULT_PAGE,
                    size=1,
                    term=None,
                    sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
                    direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
                )
            )

            assert results == expected

            # Change page
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/",
                query_string=dict(page=2, size=1),
                follow_redirects=True,
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=2,
                    size=1,
                    term=None,
                    sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
                    direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Search
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/",
                query_string=dict(term="ari"),
                follow_redirects=True,
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=ANTENNAS_DEFAULT_PAGE,
                    size=ANTENNAS_DEFAULT_PAGE_SIZE,
                    term="ari",
                    sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
                    direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Sort
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/",
                query_string=dict(sortBy="name", sortDirection="asc"),
                follow_redirects=True,
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=ANTENNAS_DEFAULT_PAGE,
                    size=ANTENNAS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by="name",
                    direction="asc",
                )
            )
            assert results == expected

            # Filter by agency
            results = client.get(
                f"/api/{BASE_ROUTE}/antennas/",
                query_string=dict(agency_id=2),
                follow_redirects=True,
            ).get_json()
            expected = AntennaPaginatedSchema().dump(
                get_all_fake_data(
                    page=ANTENNAS_DEFAULT_PAGE,
                    size=ANTENNAS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=ANTENNAS_DEFAULT_SORT_FIELD,
                    direction=ANTENNAS_DEFAULT_SORT_DIRECTION,
                    agency_id=2,
                )
            )
            assert results == expected

    @patch.object(AntennaService, "create", fake_create_antenna)
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(
                name=ANTENNA_NAME_ONE,
                postal_address=ANTENNA_ADDRESS_ONE,
                email_address=ANTENNA_EMAIL_ONE,
                agency_id=1,
            )

            # Test with unknown agency
            result = client.post(f"/api/{BASE_ROUTE}/antennas/", json=payload)
            assert result.status_code == 404
            response = result.get_json()
            assert response.get("key") == "AGENCY_NOT_FOUND_EXCEPTION"

            # Test with known agency
            payload["agency_id"] = 2
            expected = AntennaSchema().dump(
                Antenna(
                    id=1,
                    name=payload["name"],
                    postal_address=payload["postal_address"],
                    email_address=payload["email_address"],
                    agency_id=payload["agency_id"],
                )
            )
            result = client.post(
                f"/api/{BASE_ROUTE}/antennas/", json=payload
            ).get_json()
            assert result == expected


def fake_update(antenna: Antenna, changes: AntennaInterface) -> Antenna:
    # To fake an update, just return a new object
    updated_antenna = Antenna(
        id=antenna.id,
        name=changes["name"],
        postal_address=changes["postal_address"],
        email_address=changes["email_address"],
        agency_id=changes["agency_id"],
    )
    return updated_antenna


class TestAntennaIdResource:
    @patch.object(AntennaService, "get_by_id", lambda id: make_antenna(id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/antennas/123").get_json()
            expected = Antenna(id=123)
            assert result["id"] == expected.id

    @patch.object(AntennaService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/antennas/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(AntennaService, "get_by_id", lambda id: make_antenna(id=id))
    @patch.object(AntennaService, "update", fake_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/antennas/123",
                json={
                    "name": ANTENNA_NAME_ONE,
                    "postal_address": ANTENNA_ADDRESS_ONE,
                    "email_address": ANTENNA_EMAIL_ONE,
                    "agency_id": 1,
                },
            ).get_json()
            expected = AntennaSchema().dump(
                Antenna(
                    id=123,
                    name=ANTENNA_NAME_ONE,
                    postal_address=ANTENNA_ADDRESS_ONE,
                    email_address=ANTENNA_EMAIL_ONE,
                    agency_id=1,
                )
            )
            assert result == expected
