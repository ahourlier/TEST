from typing import List
from unittest.mock import patch

from flask_sqlalchemy import SQLAlchemy, Pagination

import pytest
from pytest import fixture

from app.test.fixtures import app, db
from .exceptions import UserNotFoundException, UnknownConnexionEmail, InactiveUser

from .interface import UserInterface
from .interface_test import get_user_one_interface
from .model import User
from .model_test import (
    create_user_one,
    create_user_two,
    create_user_one_not_connected,
    create_user_two_not_connected,
    USER_TWO_UID,
    USER_TWO_EMAIL,
    USER_ONE_UID,
    USER_ONE_EMAIL,
)
from .service import UserService
from ...common.group_utils import GroupUtils


@fixture
def user_one(db: SQLAlchemy) -> User:
    u1: User = create_user_one()
    db.session.add(u1)
    db.session.commit()
    return u1


@fixture
def user_two(db: SQLAlchemy) -> User:
    u2: User = create_user_two()
    db.session.add(u2)
    db.session.commit()
    return u2


def test_get_all(db: SQLAlchemy):
    u_1: User = create_user_one()
    u_2: User = create_user_two()

    db.session.add(u_1)
    db.session.add(u_2)
    db.session.commit()

    # Test with default params
    results: Pagination = UserService.get_all()
    assert results.total == 2
    assert len(results.items) == 2
    assert u_1 in results.items and u_2 in results.items

    # Test size change
    results: Pagination = UserService.get_all(size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert u_1 in results.items

    # Test page change
    results: Pagination = UserService.get_all(page=2, size=1)
    assert results.total == 2
    assert len(results.items) == 1
    assert u_2 in results.items

    # Test kind column
    results: Pagination = UserService.get_all(kind="employee")
    assert results.total == 1
    assert len(results.items) == 1
    assert u_1 in results.items

    # Test search
    results: Pagination = UserService.get_all(term="ohn")
    assert results.total == 1
    assert len(results.items) == 1
    assert u_2 in results.items

    # Test sort
    results: Pagination = UserService.get_all(sort_by="last_name", direction="asc")
    assert len(results.items) == 2
    assert results.items[0] == u_2 and results.items[1] == u_1


@patch.object(GroupUtils, "is_member_of", lambda x, y: True)
def test_create(db: SQLAlchemy):
    u1: UserInterface = get_user_one_interface()
    UserService.create(u1)
    results: List[User] = User.query.all()

    assert len(results) == 1
    for k in u1.keys():
        assert getattr(results[0], k) == u1[k]


def test_get_by_id(db: SQLAlchemy):
    u1: User = create_user_one()
    db.session.add(u1)
    with pytest.raises(UserNotFoundException) as excinfo:
        UserService.get_by_id(42)
    assert excinfo.type == UserNotFoundException
    db_user = UserService.get_by_id(u1.id)
    assert db_user == u1


def test_get_by_email(db: SQLAlchemy):
    u1: User = create_user_one()
    db.session.add(u1)

    db_user_1 = UserService.get_by_email("a.user.one@email.com")
    db_user_2 = UserService.get_by_email("inexistant.email@gmail.com")
    assert db_user_1 == u1
    assert db_user_2 == None


def test_update(db: SQLAlchemy):
    u1: User = create_user_one()
    db.session.add(u1)
    db.session.commit()

    # Test with a real change
    change_1: UserInterface = UserInterface(first_name="New User One")
    UserService.update(u1, change_1)
    result_1: User = User.query.get(u1.id)
    assert result_1.first_name == "New User One"

    # Test with no change
    previous_updated_date = result_1.updated_at
    UserService.update(u1, change_1)
    result_2: User = User.query.get(u1.id)
    assert previous_updated_date == result_2.updated_at

    # Test with no change but forced update
    previous_updated_date = result_2.updated_at
    UserService.update(u1, change_1, force_update=True)
    result_3: User = User.query.get(u1.id)
    assert previous_updated_date < result_3.updated_at


@patch.object(UserService, "get_user_info_from_gsuite", lambda x: {})
def test_update_auth_informations(db: SQLAlchemy):

    u1: User = create_user_one_not_connected()
    u2: User = create_user_two_not_connected()
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    auth_u1 = UserInterface(
        uid=USER_ONE_UID,
        email=USER_ONE_EMAIL,
    )
    auth_u2 = UserInterface(
        uid=USER_TWO_UID,
        email=USER_TWO_EMAIL,
    )
    bad_auth = UserInterface(
        uid="djksh",
        email="unknonw.email@gmail.com",
    )

    current_u1 = UserService.check_auth_informations(auth_u1["email"], auth_u1)
    assert current_u1.uid == auth_u1["uid"]

    with pytest.raises(InactiveUser) as excinfo:
        UserService.check_auth_informations(auth_u2["email"], auth_u2)
    assert excinfo.type == InactiveUser

    with pytest.raises(UnknownConnexionEmail) as excinfo:
        UserService.check_auth_informations(bad_auth["email"], bad_auth)
    assert excinfo.type == UnknownConnexionEmail


def test_has_changed(db: SQLAlchemy):
    u1: User = create_user_one()
    db.session.add(u1)
    db.session.commit()

    changes: UserInterface = UserInterface(first_name="Robert")
    assert UserService.has_changed(u1, changes) is False

    changes_2: UserInterface = UserInterface(first_name="New User One")
    assert UserService.has_changed(u1, changes_2) is True


def test_delete_by_id(db: SQLAlchemy):
    u1: User = create_user_one()
    u2: User = create_user_two()

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    deleted_id = UserService.delete_by_id(1)
    db.session.commit()

    with pytest.raises(UserNotFoundException) as excinfo:
        UserService.delete_by_id(3)
    assert excinfo.type == UserNotFoundException

    results: List[User] = User.query.all()

    assert len(results) == 1
    assert u1 not in results and u2 in results
    assert deleted_id == 1
