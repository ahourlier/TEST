from pytest import fixture

from .interface import UserInterface
from .model import User, UserKind
from .model_test import (
    USER_ONE_UID,
    USER_ONE_EMAIL,
    USER_ONE_FIRST_NAME,
    USER_ONE_LAST_NAME,
    USER_ONE_COMMENT,
    USER_ONE_ROLE,
)


def get_user_one_interface() -> UserInterface:
    return UserInterface(
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


@fixture
def interface() -> UserInterface:
    return get_user_one_interface()


def test_user_interface_create(interface: UserInterface):
    assert interface


def test_user_interface_ok(interface: UserInterface):
    user = User(**interface)
    assert user
