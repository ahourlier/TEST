from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app.test.fixtures import app, db

from .model import User, UserKind, UserRole

USER_ONE_UID = "abdcefg1234"
USER_ONE_EMAIL = "a.user.one@email.com"
USER_ONE_LAST_NAME = "Pichon"
USER_ONE_FIRST_NAME = "Robert"
USER_ONE_COMMENT = "Tel commentaire"
USER_ONE_ROLE = UserRole.ADMIN

USER_TWO_UID = "hijklmn6789"
USER_TWO_EMAIL = "b.user.two@email.com"
USER_TWO_LAST_NAME = "Edouardo"
USER_TWO_FIRST_NAME = "John"
USER_TWO_COMMENT = "Un second commentaire"
USER_TWO_ROLE = UserRole.MANAGER


def create_user_one() -> User:
    return User(
        id=1,
        uid=USER_ONE_UID,
        email=USER_ONE_EMAIL,
        first_name=USER_ONE_FIRST_NAME,
        last_name=USER_ONE_LAST_NAME,
        comment=USER_ONE_COMMENT,
        role=USER_ONE_ROLE,
        kind=UserKind.EMPLOYEE,
        active=True,
    )


def create_user_one_not_connected() -> User:
    return User(
        id=1,
        email=USER_ONE_EMAIL,
        first_name=USER_ONE_FIRST_NAME,
        last_name=USER_ONE_LAST_NAME,
        comment=USER_ONE_COMMENT,
        role=USER_ONE_ROLE,
        kind=UserKind.EMPLOYEE,
        active=True,
    )


def create_user_two() -> User:
    return User(
        id=2,
        uid=USER_TWO_UID,
        email=USER_TWO_EMAIL,
        first_name=USER_TWO_FIRST_NAME,
        last_name=USER_TWO_LAST_NAME,
        comment=USER_TWO_COMMENT,
        role=USER_TWO_ROLE,
        kind=UserKind.OTHER,
        active=True,
    )


def create_user_two_not_connected() -> User:
    return User(
        id=2,
        email=USER_TWO_EMAIL,
        first_name=USER_TWO_FIRST_NAME,
        last_name=USER_TWO_LAST_NAME,
        comment=USER_TWO_COMMENT,
        role=USER_TWO_ROLE,
        kind=UserKind.OTHER,
        active=False,
    )


@fixture
def user() -> User:
    return create_user_one()


def test_user_create(user: User):
    assert user


def test_user_retrieve(user: User, db: SQLAlchemy):
    db.session.add(user)
    db.session.commit()
    s = User.query.first()
    assert s.__dict__ == user.__dict__


def test_user_update(user: User, db: SQLAlchemy):
    db.session.add(user)
    db.session.commit()
    user.first_name = "Pierre"
    db.session.add(user)
    db.session.commit()

    assert user.first_name == "Pierre"
    assert user.updated_at is not None
