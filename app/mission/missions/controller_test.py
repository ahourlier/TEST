from datetime import date
from unittest.mock import patch

from flask.testing import FlaskClient

from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.antennas.exceptions import AntennaNotFoundException
from app.admin.clients.exceptions import ClientNotFoundException
from app.mission import BASE_ROUTE
from app.mission.missions import Mission
from app.mission.missions.interface import MissionInterface
from app.mission.missions.test.fixtures import (
    MISSION_NAME_ONE,
    MISSION_COMMENT_ONE,
    MISSION_STATUS_ONE,
    MISSION_START_DATE_ONE,
    MISSION_END_DATE_ONE,
    MISSION_NAME_TWO,
    MISSION_STATUS_TWO,
    MISSION_COMMENT_TWO,
    MISSION_START_DATE_TWO,
    MISSION_END_DATE_TWO,
)
from app.mission.missions.schema import MissionPaginatedSchema, MissionSchema
from app.mission.missions.service import (
    MissionService,
    MISSIONS_DEFAULT_PAGE,
    MISSIONS_DEFAULT_PAGE_SIZE,
    MISSIONS_DEFAULT_SORT_FIELD,
    MISSIONS_DEFAULT_SORT_DIRECTION,
)
from app.test.fixtures import app, client
from app.test.helpers import make_pagination


def make_mission(
    id: int = 1,
    name: str = MISSION_NAME_ONE,
    status: int = MISSION_STATUS_ONE,
    comment: str = MISSION_COMMENT_ONE,
    # start_date: date = MISSION_START_DATE_ONE,
    # end_date: date = MISSION_END_DATE_ONE,
    agency_id: int = 1,
    antenna_id: int = 1,
    client_id: int = 1,
) -> Mission:
    return Mission(
        id=id,
        name=name,
        status=status,
        comment=comment,
        # start_date = start_date,
        # end_date = end_date,
        agency_id=agency_id,
        antenna_id=antenna_id,
        client_id=client_id,
    )


def get_all_fake_data(**kwargs):
    m1 = make_mission(
        123,
        name=MISSION_NAME_ONE,
        status=MISSION_STATUS_ONE,
        comment=MISSION_COMMENT_ONE,
        # start_date: date = MISSION_START_DATE_ONE,
        # end_date: date = MISSION_END_DATE_ONE,
        agency_id=1,
        antenna_id=1,
        client_id=1,
    )
    m2 = make_mission(
        456,
        name=MISSION_NAME_TWO,
        comment=MISSION_COMMENT_TWO,
        status=MISSION_STATUS_TWO,
        # start_date= MISSION_START_DATE_TWO,
        # end_date= MISSION_END_DATE_TWO,
        agency_id=1,
        antenna_id=1,
        client_id=1,
    )

    items = [m1, m2]
    total = 2
    if (
        kwargs.get("term") == "ion2"
        or kwargs.get("agency_id") == 2
        or kwargs.get("antenna_id") == 2
        or kwargs.get("client_id") == 2
    ):
        items = [m2]
        total = 1
    elif kwargs.get("size") == 1:
        if kwargs.get("page") == 1:
            items = [m1]
        elif kwargs.get("page") == 2:
            items = [m2]
    elif kwargs.get("direction") == "asc" and kwargs.get("sort_by") == "name":
        items = [m2, m1]

    return make_pagination(
        items=items, page=kwargs.get("page"), per_page=kwargs.get("size"), total=total,
    )


def fake_create_mission(*args):
    mission_interface = args[0]
    if mission_interface.get("agency_id") == 1:
        raise AgencyNotFoundException
    if mission_interface.get("antenna_id") == 1:
        raise AntennaNotFoundException
    if mission_interface.get("client_id") == 1:
        raise ClientNotFoundException
    return make_mission(agency_id=2, antenna_id=2, client_id=2)


class TestMissionResource:
    @patch.object(MissionService, "get_all", get_all_fake_data)
    def test_get(self, client: FlaskClient):
        with client:
            # Test with no query parameters
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/", follow_redirects=True
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Change size
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(size=1),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=1,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                )
            )

            assert results == expected

            # Change page
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(page=2, size=1),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=2,
                    size=1,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Search
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(term="ion2"),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term="ion2",
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Sort
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(sortBy="name", sortDirection="asc"),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by="name",
                    direction="asc",
                )
            )
            assert results == expected

            # Filter by agency
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(agency_id=2),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                    agency_id=2,
                )
            )
            assert results == expected

            # Filter by antenna
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(antenna_id=2),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                    antenna_id=2,
                )
            )
            assert results == expected

            # Filter by client
            results = client.get(
                f"/api/{BASE_ROUTE}/missions/",
                query_string=dict(client_id=2),
                follow_redirects=True,
            ).get_json()
            expected = MissionPaginatedSchema().dump(
                get_all_fake_data(
                    page=MISSIONS_DEFAULT_PAGE,
                    size=MISSIONS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=MISSIONS_DEFAULT_SORT_FIELD,
                    direction=MISSIONS_DEFAULT_SORT_DIRECTION,
                    client_id=2,
                )
            )
            assert results == expected

    @patch.object(MissionService, "create", fake_create_mission)
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(
                name=MISSION_NAME_ONE,
                status=MISSION_STATUS_ONE,
                comment=MISSION_COMMENT_ONE,
                # start_date: date = MISSION_START_DATE_ONE,
                # end_date: date = MISSION_END_DATE_ONE,
                agency_id=2,
                antenna_id=2,
                client_id=2,
            )

            # Test with unknown agency
            payload["agency_id"] = 1
            result = client.post(f"/api/{BASE_ROUTE}/missions/", json=payload)
            assert result.status_code == 404
            response = result.get_json()
            assert response.get("key") == "AGENCY_NOT_FOUND_EXCEPTION"

            # Test with unknown antenna
            payload["agency_id"] = 2
            payload["antenna_id"] = 1
            result = client.post(f"/api/{BASE_ROUTE}/missions/", json=payload)
            assert result.status_code == 404
            response = result.get_json()
            assert response.get("key") == "ANTENNA_NOT_FOUND_EXCEPTION"

            # Test with unknown client
            payload["antenna_id"] = 2
            payload["client_id"] = 1
            result = client.post(f"/api/{BASE_ROUTE}/missions/", json=payload)
            assert result.status_code == 404
            response = result.get_json()
            assert response.get("key") == "CLIENT_NOT_FOUND_EXCEPTION"

            # Test with correct relational values
            payload["client_id"] = 2
            expected = MissionSchema().dump(
                Mission(
                    id=1,
                    name=payload["name"],
                    status=payload["status"],
                    comment=payload["comment"],
                    # start_date=payload["start_date"],
                    # end_date=payload["end_date"],
                    agency_id=payload["agency_id"],
                    antenna_id=payload["antenna_id"],
                    client_id=payload["client_id"],
                )
            )

            result = client.post(
                f"/api/{BASE_ROUTE}/missions/", json=payload
            ).get_json()
            assert result == expected


def fake_update(mission: Mission, changes: MissionInterface) -> Mission:
    # To fake an update, just return a new object
    updated_mission = Mission(
        id=mission.id,
        name=changes["name"],
        status=changes["status"],
        comment=changes["comment"],
        # start_date=changes["start_date"],
        # end_date=changes["end_date"],
        antenna_id=changes["antenna_id"],
        client_id=changes["client_id"],
        agency_id=changes["agency_id"],
    )
    return updated_mission


class TestMissionIdResource:
    @patch.object(MissionService, "get_by_id", lambda id: make_mission(id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/missions/123").get_json()
            expected = Mission(id=123)
            assert result["id"] == expected.id

    @patch.object(MissionService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/missions/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(MissionService, "get_by_id", lambda id: make_mission(id=id))
    @patch.object(MissionService, "update", fake_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/missions/123",
                json={
                    "name": MISSION_NAME_ONE,
                    "status": MISSION_STATUS_ONE,
                    "comment": MISSION_COMMENT_ONE,
                    # "start_date": MISSION_START_DATE_ONE,
                    # "end_date": MISSION_END_DATE_ONE,
                    "antenna_id": 1,
                    "client_id": 1,
                    "agency_id": 1,
                },
            ).get_json()
            expected = MissionSchema().dump(
                Mission(
                    id=123,
                    name=MISSION_NAME_ONE,
                    status=MISSION_STATUS_ONE,
                    comment=MISSION_COMMENT_ONE,
                    # start_date=MISSION_START_DATE_ONE,
                    # end_date=MISSION_END_DATE_ONE,
                    antenna_id=1,
                    client_id=1,
                    agency_id=1,
                )
            )
            assert result == expected
