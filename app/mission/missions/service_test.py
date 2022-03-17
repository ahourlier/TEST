from typing import List
from unittest.mock import patch

from flask_sqlalchemy import SQLAlchemy, Pagination
from pytest import fixture
import pytest

from app.admin.agencies import Agency
from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.agencies.model_test import create_agency_one, create_agency_two
from app.admin.antennas import Antenna
from app.admin.antennas.exceptions import AntennaNotFoundException
from app.admin.antennas.model_test import create_antenna_one
from app.admin.clients import Client
from app.admin.clients.exceptions import ClientNotFoundException
from app.admin.clients.model_test import create_client_one
from app.auth.users.model_test import create_user_one
from app.common.exceptions import InconsistentUpdateIdException
from app.mission.missions import Mission
from app.mission.missions.error_handlers import MissionNotFoundException
from app.mission.missions.interface import MissionInterface
from app.mission.missions.interface_test import get_mission_one_interface

from app.mission.missions.service import MissionService

# IMPORT FIXTURES
from app.mission.missions.test.fixtures import (
    create_mission_one,
    create_mission_two,
    MISSION_NAME_ONE,
    MISSION_STATUS_ONE,
    MISSION_COMMENT_ONE,
    MISSION_START_DATE_ONE,
    MISSION_END_DATE_ONE,
)
from app.test.fixtures import app, db
from app.admin.antennas.test.fixtures import antenna_one, antenna_two
from app.admin.agencies.test.fixtures import agency_one, agency_two
from app.admin.clients.test.fixtures import client_one, client_two


def test_get_all(
    agency_one: Agency,
    agency_two: Agency,
    antenna_one: Antenna,
    antenna_two: Antenna,
    client_one: Client,
    client_two: Client,
    db: SQLAlchemy,
):
    user_one = create_user_one()
    mission_1: Mission = create_mission_one(
        agency_one.id, antenna_one.id, client_one.id
    )
    mission_2: Mission = create_mission_two(
        agency_one.id, antenna_one.id, client_one.id
    )

    db.session.add(mission_1)
    db.session.add(mission_2)
    db.session.commit()

    results: Pagination = MissionService.get_all(user=user_one)

    assert results.total == 2
    assert len(results.items) == 2
    assert mission_1 in results.items and mission_2 in results.items

    # Test size change
    results: Pagination = MissionService.get_all(size=1, user=user_one)
    assert results.total == 2
    assert len(results.items) == 1
    assert mission_2 in results.items

    # Test page change
    results: Pagination = MissionService.get_all(page=2, size=1, user=user_one)
    assert results.total == 2
    assert len(results.items) == 1
    assert mission_1 in results.items

    # Test search
    results: Pagination = MissionService.get_all(term="on2", user=user_one)
    assert results.total == 1
    assert len(results.items) == 1
    assert mission_2 in results.items

    # Test sort by name
    results: Pagination = MissionService.get_all(
        sort_by="name", direction="asc", user=user_one
    )
    assert len(results.items) == 2
    assert results.items[0] == mission_2 and results.items[1] == mission_1

    # Test sort by date (default missions sort field)
    results: Pagination = MissionService.get_all(direction="asc", user=user_one)
    assert len(results.items) == 2
    assert results.items[0] == mission_1 and results.items[1] == mission_2

    # Test filter by agency
    mission_2.agency_id = agency_two.id
    db.session.commit()
    results: Pagination = MissionService.get_all(agency_id=agency_two.id, user=user_one)
    assert len(results.items) == 1
    assert results.items[0] == mission_2

    # Test filter by antenna
    mission_2.antenna_id = antenna_two.id
    db.session.commit()
    results: Pagination = MissionService.get_all(
        antenna_id=antenna_two.id, user=user_one
    )
    assert len(results.items) == 1
    assert results.items[0] == mission_2

    # Test filter by client
    mission_2.client_id = client_two.id
    db.session.commit()
    results: Pagination = MissionService.get_all(client_id=client_two.id, user=user_one)
    assert len(results.items) == 1
    assert results.items[0] == mission_2


def test_create_bad_relations(
    agency_one: Agency, antenna_one: Antenna,
):
    mission_1: MissionInterface = get_mission_one_interface()

    # Test mission creation with an id matching with no existing antenna
    mission_1["antenna_id"] = 42
    with pytest.raises(AntennaNotFoundException) as e:
        MissionService.create(mission_1)
    assert e.type == AntennaNotFoundException

    # Test mission creation with an id matching with no existing agency
    mission_1["antenna_id"] = antenna_one.id
    mission_1["agency_id"] = 42
    with pytest.raises(AgencyNotFoundException) as e:
        MissionService.create(mission_1)
    assert e.type == AgencyNotFoundException

    # Test mission creation with an id matching with no existing client
    mission_1["agency_id"] = agency_one.id
    mission_1["client_id"] = 42
    with pytest.raises(ClientNotFoundException) as e:
        MissionService.create(mission_1)
    assert e.type == ClientNotFoundException


def test_get_by_id(
    agency_one: Agency, antenna_one: Antenna, client_one: Client, db: SQLAlchemy
):
    m1: Antenna = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)

    db_antenna = MissionService.get_by_id(1)

    with pytest.raises(MissionNotFoundException) as excinfo:
        MissionService.get_by_id(42)
    assert excinfo.type == MissionNotFoundException

    assert db_antenna == m1


def test_create(
    db: SQLAlchemy, agency_one: Agency, antenna_one: Antenna, client_one: Client,
):
    mission_1: MissionInterface = get_mission_one_interface()

    with patch("app.mission.missions.service.create_task", return_value=True):
        with patch("app.mission.missions.service.request", return_value=object()):
            new_mission: Mission = MissionService.create(mission_1)
    db.session.add(new_mission)
    db.session.commit()
    user = create_user_one()
    results = MissionService.get_all(user=user)
    assert len(results.items) == 1
    assert results.items[0].name == MISSION_NAME_ONE
    assert results.items[0].status == MISSION_STATUS_ONE
    assert results.items[0].comment == MISSION_COMMENT_ONE
    assert results.items[0].start_date == MISSION_START_DATE_ONE
    assert results.items[0].end_date == MISSION_END_DATE_ONE
    assert results.items[0].agency_id == agency_one.id
    assert results.items[0].antenna_id == antenna_one.id
    assert results.items[0].client_id == client_one.id


def test_update(
    agency_one: Agency, antenna_one: Antenna, client_one: Client, db: SQLAlchemy
):

    # Test with real change
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    change_1: MissionInterface = MissionInterface(name="MissionImpossible")
    MissionService.update(m1, change_1)
    result_1: Mission = Mission.query.get(1)
    assert result_1.name == "MissionImpossible"

    # Test with no change
    previous_updated_date = result_1.updated_at
    MissionService.update(m1, change_1)
    result_2: Mission = Mission.query.get(1)
    assert previous_updated_date == result_2.updated_at

    # Test with no change but forced update
    previous_updated_date = result_2.updated_at
    MissionService.update(m1, change_1, force_update=True)
    result_3: Mission = Mission.query.get(1)
    assert previous_updated_date < result_3.updated_at


def test_update_inconsistent_id(
    agency_one: Agency, antenna_one: Antenna, client_one: Client, db: SQLAlchemy
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    inconsistent_change: MissionInterface = MissionInterface(id=42)
    with pytest.raises(InconsistentUpdateIdException) as excinfo:
        MissionService.update(m1, inconsistent_change)
    assert excinfo.type == InconsistentUpdateIdException


def test_update_change_agency(
    agency_one: Agency,
    agency_two: Agency,
    antenna_one: Antenna,
    client_one: Client,
    db: SQLAlchemy,
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    change_agency: MissionInterface = MissionInterface(agency_id=agency_two.id)
    MissionService.update(m1, change_agency)
    result: Mission = Mission.query.get(1)
    assert result.agency == agency_two
    assert agency_two.missions[0] == result


def test_update_change_antenna(
    agency_one: Agency,
    antenna_one: Antenna,
    antenna_two: Antenna,
    client_one: Client,
    db: SQLAlchemy,
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    change_agency: MissionInterface = MissionInterface(antenna_id=antenna_two.id)
    MissionService.update(m1, change_agency)
    result: Mission = Mission.query.get(1)
    assert result.antenna == antenna_two
    assert antenna_two.missions[0] == result


def test_update_change_client(
    agency_one: Agency,
    antenna_one: Antenna,
    client_one: Client,
    client_two: Client,
    db: SQLAlchemy,
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    change_agency: MissionInterface = MissionInterface(client_id=client_two.id)
    MissionService.update(m1, change_agency)
    result: Mission = Mission.query.get(1)
    assert result.client == client_two
    assert client_two.missions[0] == result


def test_has_changed(
    agency_one: Agency, antenna_one: Antenna, client_one: Client, db: SQLAlchemy
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    changes: MissionInterface = MissionInterface(name=m1.name)
    assert MissionService.has_changed(m1, changes) is False

    changes_2: MissionInterface = MissionInterface(name="MissionPossible")
    assert MissionService.has_changed(m1, changes_2) is True


def test_delete_by_id(
    agency_one: Agency, antenna_one: Antenna, client_one: Client, db: SQLAlchemy,
):
    m1: Mission = create_mission_one(agency_one.id, antenna_one.id, client_one.id)
    db.session.add(m1)
    db.session.commit()

    deleted_id = MissionService.delete_by_id(1)
    db.session.commit()

    with pytest.raises(MissionNotFoundException) as excinfo:
        MissionService.delete_by_id(42)
    assert excinfo.type == MissionNotFoundException

    results: List[Mission] = Mission.query.all()

    assert len(results) == 1
    assert m1 in results
    assert results[0].is_deleted is True
    assert deleted_id == 1
