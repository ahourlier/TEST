from typing import List

import pytest
from flask_sqlalchemy import SQLAlchemy, Pagination
from pytest import fixture

from app.admin.agencies import Agency
from app.admin.agencies.exceptions import AgencyNotFoundException
from app.admin.agencies.model_test import create_agency_one, create_agency_two
from app.admin.antennas import Antenna
from app.admin.antennas.exceptions import AntennaNotFoundException
from app.admin.antennas.interface import AntennaInterface
from app.admin.antennas.interface_test import get_antenna_one_interface
from app.admin.antennas.model_test import (
    create_antenna_one,
    create_antenna_two,
    ANTENNA_NAME_ONE,
    ANTENNA_ADDRESS_ONE,
    ANTENNA_EMAIL_ONE,
)
from app.admin.antennas.service import AntennaService
from app.common.exceptions import InconsistentUpdateIdException
from app.test.fixtures import app, db
from app.admin.agencies.test.fixtures import agency_one, agency_two


def test_get_all(agency_one: Agency, db: SQLAlchemy):
    ant_1: Antenna = create_antenna_one(agency_one.id)
    ant_2: Antenna = create_antenna_two(agency_one.id)

    db.session.add(ant_1)
    db.session.add(ant_2)
    db.session.commit()

    # Test with default params

    results: Pagination = AntennaService.get_all()

    assert results.total == 2
    assert len(results.items) == 2
    assert ant_1 in results.items and ant_2 in results.items

    # Test size change
    results: Pagination = AntennaService.get_all(size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert ant_2 in results.items

    # Test page change
    results: Pagination = AntennaService.get_all(page=2, size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert ant_1 in results.items

    # Test search
    results: Pagination = AntennaService.get_all(term="auro")
    assert results.total == 1
    assert len(results.items) == 1
    assert ant_2 in results.items

    # Test sort
    results: Pagination = AntennaService.get_all(sort_by="name", direction="asc")
    assert len(results.items) == 2
    assert results.items[0] == ant_2 and results.items[1] == ant_1

    # Test filter by agency
    agency_two = create_agency_two()
    ant_2.agency = agency_two
    db.session.add(agency_two)
    db.session.add(ant_2)
    db.session.commit()

    results: Pagination = AntennaService.get_all(agency_id=agency_two.id)
    assert len(results.items) == 1
    assert results.items[0] == ant_2


def test_get_by_id(agency_one: Agency, db: SQLAlchemy):
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)

    db_antenna = AntennaService.get_by_id(1)

    with pytest.raises(AntennaNotFoundException) as excinfo:
        AntennaService.get_by_id(42)
    assert excinfo.type == AntennaNotFoundException

    assert db_antenna == a1


def test_create(db: SQLAlchemy):
    ant_1: AntennaInterface = get_antenna_one_interface()
    with pytest.raises(AgencyNotFoundException) as e:
        AntennaService.create(ant_1)

    assert e.type == AgencyNotFoundException

    a1: Agency = create_agency_one()
    db.session.add(a1)
    db.session.commit()
    ant_1["agency_id"] = a1.id

    new_antenna: Antenna = AntennaService.create(ant_1)
    db.session.add(new_antenna)
    db.session.commit()
    results = AntennaService.get_all()
    assert len(results.items) == 1
    assert results.items[0].name == ANTENNA_NAME_ONE
    assert results.items[0].postal_address == ANTENNA_ADDRESS_ONE
    assert results.items[0].email_address == ANTENNA_EMAIL_ONE
    assert results.items[0].agency_id == a1.id


def test_update(agency_one: Agency, db: SQLAlchemy):

    # Test with real change
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)
    db.session.commit()

    change_1: AntennaInterface = AntennaInterface(name="Mulhouse")
    AntennaService.update(a1, change_1)
    result_1: Antenna = Antenna.query.get(1)
    assert result_1.name == "Mulhouse"

    # Test with no change
    previous_updated_date = result_1.updated_at
    AntennaService.update(a1, change_1)
    result_2: Antenna = Antenna.query.get(1)
    assert previous_updated_date == result_2.updated_at

    # Test with no change but forced update
    previous_updated_date = result_2.updated_at
    AntennaService.update(a1, change_1, force_update=True)
    result_3: Antenna = Antenna.query.get(1)
    assert previous_updated_date < result_3.updated_at


def test_update_inconsistent_id(agency_one: Agency, db: SQLAlchemy):
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)
    db.session.commit()

    inconsistent_change: AntennaInterface = AntennaInterface(id=42)
    with pytest.raises(InconsistentUpdateIdException) as excinfo:
        AntennaService.update(a1, inconsistent_change)
    assert excinfo.type == InconsistentUpdateIdException


def test_update_change_agency(agency_one: Agency, agency_two: Agency, db: SQLAlchemy):
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)
    db.session.commit()

    change_agency: AntennaInterface = AntennaInterface(
        agency_id=agency_two.id, name=ANTENNA_NAME_ONE
    )
    AntennaService.update(a1, change_agency)
    result: Antenna = Antenna.query.get(1)
    assert result.agency == agency_two
    assert agency_two.antennas[0] == result


def test_has_changed(agency_one: Agency, db: SQLAlchemy):
    a1: Antenna = create_antenna_one(agency_one.id)
    db.session.add(a1)
    db.session.commit()

    changes: AntennaInterface = AntennaInterface(name=a1.name)
    assert AntennaService.has_changed(a1, changes) is False

    changes_2: AntennaInterface = AntennaInterface(name="Mulhouse")
    assert AntennaService.has_changed(a1, changes_2) is True


def test_delete_by_id(agency_one: Agency, agency_two: Agency, db: SQLAlchemy):
    a1: Antenna = create_antenna_one(agency_one.id)
    a2: Antenna = create_antenna_two(agency_two.id)
    db.session.add(a1)
    db.session.add(a2)
    db.session.commit()

    deleted_id = AntennaService.delete_by_id(1)
    db.session.commit()

    with pytest.raises(AntennaNotFoundException) as excinfo:
        AntennaService.delete_by_id(3)
    assert excinfo.type == AntennaNotFoundException

    results: List[Antenna] = Antenna.query.all()

    assert agency_one.antennas == []
    assert len(results) == 1
    assert a1 not in results and a2 in results
    assert deleted_id == 1
