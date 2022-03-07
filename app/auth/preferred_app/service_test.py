from flask_sqlalchemy import SQLAlchemy
from app.test.fixtures import app, db
from .interface import PreferredAppInterface
from .model import PreferredApp
from .service import PreferredAppService
from ..users import User
from ..users.interface import UserInterface
from ..users.model import UserKind
from ..users.model_test import (
    USER_ONE_UID,
    USER_ONE_EMAIL,
    USER_ONE_FIRST_NAME,
    USER_ONE_LAST_NAME,
    USER_ONE_COMMENT,
    USER_ONE_ROLE,
)
from ...common import Role
from ...common.app_name import App

mock_preferred_app = PreferredAppInterface(
    **{"preferred_app": App.INDIVIDUAL, "first_connection": True}
)

mock_user = User(
    uid=USER_ONE_UID,
    email=USER_ONE_EMAIL,
    first_name=USER_ONE_FIRST_NAME,
    last_name=USER_ONE_LAST_NAME,
    comment=USER_ONE_COMMENT,
    role=USER_ONE_ROLE,
    kind=UserKind.EMPLOYEE,
    active=True,
)


def test_create(db: SQLAlchemy):
    preferred_apps = PreferredApp.query.all()
    assert len(preferred_apps) == 0
    res = PreferredAppService.create(mock_preferred_app)
    preferred_app = PreferredApp.query.first()
    assert preferred_app is not None
    assert preferred_app.preferred_app == mock_preferred_app.get("preferred_app")
    assert preferred_app.first_connection == mock_preferred_app.get("first_connection")


def test_create_for_user(db: SQLAlchemy):
    db.session.add(Role(name=USER_ONE_ROLE, value=1))
    db.session.commit()
    created_user = User(
        uid=USER_ONE_UID,
        email=USER_ONE_EMAIL,
        first_name=USER_ONE_FIRST_NAME,
        last_name=USER_ONE_LAST_NAME,
        comment=USER_ONE_COMMENT,
        role=USER_ONE_ROLE,
        kind=UserKind.EMPLOYEE,
        active=True,
    )
    db.session.add(created_user)
    db.session.commit()
    PreferredAppService.create_for_user(mock_preferred_app, created_user.id)
    updated_user = User.query.get(created_user.id)
    assert updated_user.preferred_app_id is not None
    assert updated_user.preferred_app.preferred_app == mock_preferred_app.get(
        "preferred_app"
    )
    assert updated_user.preferred_app.first_connection == mock_preferred_app.get(
        "first_connection"
    )


def test_update(db: SQLAlchemy):
    res = PreferredApp(preferred_app=App.INDIVIDUAL, first_connection=True)
    db.session.add(res)
    db.session.commit()
    new_attrs = PreferredAppInterface(preferred_app=App.COPRO)
    res = PreferredAppService.update(res.id, new_attrs)
    assert res.preferred_app == App.COPRO


def test_delete(db: SQLAlchemy):
    res = PreferredApp(preferred_app=App.INDIVIDUAL, first_connection=True)
    db.session.add(res)
    db.session.commit()
    preferred_apps = PreferredApp.query.all()
    assert len(preferred_apps) == 1
    deleted_id = PreferredAppService.delete(res.id)
    assert deleted_id == res.id
    preferred_apps = PreferredApp.query.all()
    assert len(preferred_apps) == 0
