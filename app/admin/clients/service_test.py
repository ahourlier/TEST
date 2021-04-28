from typing import List
import pytest

from flask_sqlalchemy import SQLAlchemy, Pagination
from app.test.fixtures import app, db
from .exceptions import ClientNotFoundException
from .interface import ClientInterface
from .interface_test import get_client_one_interface

from .model import Client
from .model_test import create_client_one, create_client_two
from .service import ClientService
from ...common.exceptions import InconsistentUpdateIdException


def test_get_all(db: SQLAlchemy):
    c1: Client = create_client_one()
    c2: Client = create_client_two()

    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    # Test with default params

    results: Pagination = ClientService.get_all()

    assert results.total == 2
    assert len(results.items) == 2
    assert c1 in results.items and c2 in results.items

    # Test size change
    results: Pagination = ClientService.get_all(size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert c2 in results.items

    # Test page change
    results: Pagination = ClientService.get_all(page=2, size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert c1 in results.items

    # Test search
    results: Pagination = ClientService.get_all(term="naël")
    assert results.total == 1
    assert len(results.items) == 1
    assert c2 in results.items

    # Test sort
    results: Pagination = ClientService.get_all(sort_by="name", direction="asc")
    assert len(results.items) == 2
    assert results.items[0] == c2 and results.items[1] == c1


def test_get_by_id(db: SQLAlchemy):
    c1: Client = create_client_one()
    db.session.add(c1)
    db_client = ClientService.get_by_id(1)
    with pytest.raises(ClientNotFoundException) as excinfo:
        ClientService.get_by_id(42)
    assert excinfo.type == ClientNotFoundException
    assert db_client == c1


def test_create(db: SQLAlchemy):
    c1: ClientInterface = get_client_one_interface()
    ClientService.create(c1)
    results: List[Client] = Client.query.all()

    assert len(results) == 1
    for k in c1.keys():
        assert getattr(results[0], k) == c1[k]


def test_update(db: SQLAlchemy):
    c1: Client = create_client_one()
    db.session.add(c1)
    db.session.commit()

    # Test with a real change
    change_1: ClientInterface = ClientInterface(name="Un nouveau client")
    ClientService.update(c1, change_1)
    result_1: Client = Client.query.get(1)
    assert result_1.name == "Un nouveau client"

    # Test with no change
    previous_updated_date = result_1.updated_at
    ClientService.update(c1, change_1)
    result_2: Client = Client.query.get(1)
    assert previous_updated_date == result_2.updated_at

    # Test with no change but forced update
    previous_updated_date = result_2.updated_at
    ClientService.update(c1, change_1, force_update=True)
    result_3: Client = Client.query.get(1)
    assert previous_updated_date < result_3.updated_at

    # Test with inconsistent id
    bad_change: ClientInterface = ClientInterface(id=42)
    with pytest.raises(InconsistentUpdateIdException) as excinfo:
        ClientService.update(c1, bad_change)
    assert excinfo.type == InconsistentUpdateIdException


def test_has_changed(db: SQLAlchemy):
    c1: Client = create_client_one()
    db.session.add(c1)
    db.session.commit()

    changes: ClientInterface = ClientInterface(name=c1.name)
    assert ClientService.has_changed(c1, changes) is False

    changes_2: ClientInterface = ClientInterface(name="Un nouveau client")
    assert ClientService.has_changed(c1, changes_2) is True


def test_delete_by_id(db: SQLAlchemy):
    c1: Client = create_client_one()
    c2: Client = create_client_two()

    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    deleted_id = ClientService.delete_by_id(1)

    results: List[Client] = Client.query.all()
    deleted_client = Client.query.get(deleted_id)

    assert len(results) == 2
    assert deleted_id == 1
    assert deleted_client.active == False

    with pytest.raises(ClientNotFoundException) as excinfo:
        ClientService.delete_by_id(3)
    assert excinfo.type == ClientNotFoundException
