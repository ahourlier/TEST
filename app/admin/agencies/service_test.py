from typing import List
import pytest

from flask_sqlalchemy import SQLAlchemy, Pagination
from app.test.fixtures import app, db
from .exceptions import AgencyNotFoundException

from .interface import AgencyInterface
from .interface_test import get_agency_one_interface
from .model import Agency
from app.admin.antennas.model import Antenna
from .model_test import create_agency_one, create_agency_two
from .service import AgencyService
from app.admin.error_handlers import InconsistentUpdateIdException


def test_get_all(db: SQLAlchemy):
    a1: Agency = create_agency_one()
    a2: Agency = create_agency_two()

    db.session.add(a1)
    db.session.add(a2)
    db.session.commit()

    # Test with default params

    results: Pagination = AgencyService.get_all()

    assert results.total == 2
    assert len(results.items) == 2
    assert a1 in results.items and a2 in results.items

    # Test size change
    results: Pagination = AgencyService.get_all(size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert a2 in results.items

    # Test page change
    results: Pagination = AgencyService.get_all(page=2, size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert a1 in results.items

    # Test search
    results: Pagination = AgencyService.get_all(term="ari")
    assert results.total == 1
    assert len(results.items) == 1
    assert a2 in results.items

    # Test sort
    results: Pagination = AgencyService.get_all(sort_by="name", direction="asc")
    assert len(results.items) == 2
    assert results.items[0] == a2 and results.items[1] == a1


def test_get_by_id(db: SQLAlchemy):
    a1: Agency = create_agency_one()
    db.session.add(a1)
    db_agency = AgencyService.get_by_id(1)
    with pytest.raises(AgencyNotFoundException) as excinfo:
        AgencyService.get_by_id(42)
    assert excinfo.type == AgencyNotFoundException
    assert db_agency == a1


def test_create(db: SQLAlchemy):
    a1: AgencyInterface = get_agency_one_interface()
    AgencyService.create(a1)
    results: List[Agency] = Agency.query.all()
    child_antenna: Antenna = Antenna.query.first()

    assert child_antenna is not None
    assert len(results) == 1
    for k in a1.keys():
        assert getattr(results[0], k) == a1[k]
        assert results[0].name == child_antenna.name
        assert results[0].email_address == child_antenna.email_address
        assert results[0].postal_address == child_antenna.postal_address


def test_update(db: SQLAlchemy):
    a1: Agency = create_agency_one()
    db.session.add(a1)
    db.session.commit()

    # Test with a real change
    change_1: AgencyInterface = AgencyInterface(name="Mulhouse")
    AgencyService.update(a1, change_1)
    result_1: Agency = Agency.query.get(1)
    assert result_1.name == "Mulhouse"

    # Test with no change
    previous_updated_date = result_1.updated_at
    AgencyService.update(a1, change_1)
    result_2: Agency = Agency.query.get(1)
    assert previous_updated_date == result_2.updated_at

    # Test with no change but forced update
    previous_updated_date = result_2.updated_at
    AgencyService.update(a1, change_1, force_update=True)
    result_3: Agency = Agency.query.get(1)
    assert previous_updated_date < result_3.updated_at

    # Test with inconsistent id
    bad_change: AgencyInterface = AgencyInterface(id=42)
    with pytest.raises(InconsistentUpdateIdException) as excinfo:
        AgencyService.update(a1, bad_change)
    assert excinfo.type == InconsistentUpdateIdException


def test_has_changed(db: SQLAlchemy):
    a1: Agency = create_agency_one()
    db.session.add(a1)
    db.session.commit()

    changes: AgencyInterface = AgencyInterface(name=a1.name)
    assert AgencyService.has_changed(a1, changes) is False

    changes_2: AgencyInterface = AgencyInterface(name="Mulhouse")
    assert AgencyService.has_changed(a1, changes_2) is True


def test_delete_by_id(db: SQLAlchemy):
    a1: Agency = create_agency_one()
    a2: Agency = create_agency_two()

    db.session.add(a1)
    db.session.add(a2)
    db.session.commit()

    deleted_id = AgencyService.delete_by_id(1)
    db.session.commit()

    with pytest.raises(AgencyNotFoundException) as excinfo:
        bad_delete = AgencyService.delete_by_id(3)
    assert excinfo.type == AgencyNotFoundException

    results: List[Agency] = Agency.query.all()

    assert len(results) == 1
    assert a1 not in results and a2 in results
    assert deleted_id == 1
