from pytest import fixture

from .model import User, UserKind
from .model_test import (
    USER_ONE_UID,
    USER_ONE_EMAIL,
    USER_ONE_FIRST_NAME,
    USER_ONE_LAST_NAME,
    USER_ONE_COMMENT,
    USER_ONE_ROLE,
)
from .schema import UserSchema


@fixture
def schema() -> UserSchema:
    return UserSchema()


def test_user_schema_create(schema: UserSchema):
    assert schema


def test_user_schema_ok(schema: UserSchema):
    params = schema.load(
        {
            "uid": USER_ONE_UID,
            "email": USER_ONE_EMAIL,
            "first_name": USER_ONE_FIRST_NAME,
            "last_name": USER_ONE_LAST_NAME,
            "comment": USER_ONE_COMMENT,
            "role": USER_ONE_ROLE,
            "kind": UserKind.EMPLOYEE,
            "active": True,
        }
    )

    user = User(**params)

    assert user.uid == USER_ONE_UID
    assert user.email == USER_ONE_EMAIL
    assert user.first_name == USER_ONE_FIRST_NAME
    assert user.last_name == USER_ONE_LAST_NAME
    assert user.comment == USER_ONE_COMMENT
    assert user.role == USER_ONE_ROLE
    assert user.kind == UserKind.EMPLOYEE
    assert user.active is True
