from functools import wraps
from unittest.mock import patch
from flask.testing import FlaskClient

from app.test.fixtures import client, app
from .model_test import (
    create_user_one,
    USER_ONE_EMAIL,
    USER_ONE_FIRST_NAME,
    USER_ONE_LAST_NAME,
    USER_ONE_COMMENT,
    USER_ONE_ROLE,
    USER_TWO_EMAIL,
    USER_TWO_FIRST_NAME,
    USER_TWO_LAST_NAME,
    USER_TWO_COMMENT,
    USER_TWO_ROLE,
    USER_ONE_UID,
    USER_TWO_UID,
)
from app.auth.users.schema import UserPaginatedSchema, UserAuthSchema
from .service import (
    UserService,
    USERS_DEFAULT_PAGE,
    USERS_DEFAULT_PAGE_SIZE,
    USERS_DEFAULT_SORT_FIELD,
    USERS_DEFAULT_SORT_DIRECTION,
)
from .schema import UserSchema
from .model import User, UserKind
from .interface import UserInterface
from .. import BASE_ROUTE
from ...test.helpers import make_pagination


def make_user(
    id: int = 123,
    uid: str = USER_ONE_UID,
    email: str = USER_ONE_EMAIL,
    first_name: str = USER_ONE_FIRST_NAME,
    last_name: str = USER_ONE_LAST_NAME,
    comment: str = USER_ONE_COMMENT,
    role: str = USER_ONE_ROLE,
    kind: str = UserKind.EMPLOYEE,
    active: bool = True,
) -> User:
    return User(
        id=id,
        uid=uid,
        first_name=first_name,
        last_name=last_name,
        email=email,
        comment=comment,
        role=role,
        kind=kind,
        active=active,
    )


def fake_get_all(**kwargs):
    u1 = make_user()
    u2 = make_user(
        id=456,
        uid=USER_TWO_UID,
        email=USER_TWO_EMAIL,
        first_name=USER_TWO_FIRST_NAME,
        last_name=USER_TWO_LAST_NAME,
        comment=USER_TWO_COMMENT,
        role=USER_TWO_ROLE,
    )

    items = [u1, u2]
    total = 2
    if kwargs.get("term") == "ohn":
        items = [u2]
        total = 1
    elif kwargs.get("size") == 1:
        if kwargs.get("page") == 1:
            items = [u1]
        elif kwargs.get("page") == 2:
            items = [u2]
    elif kwargs.get("direction") == "desc" and kwargs.get("sort_by") == "email":
        items = [u2, u1]

    return make_pagination(
        items=items, page=kwargs.get("page"), per_page=kwargs.get("size"), total=total,
    )


class TestUserMe:
    @patch.object(UserService, "update_user_groups", lambda x: True)
    @patch.object(UserService, "get_permissions_for_role", lambda x: [])
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(
                f"/api/{BASE_ROUTE}/users/me", follow_redirects=True
            ).get_json()
            user_one = create_user_one()
            setattr(user_one, "permissions", [])
            expected = UserAuthSchema().dump(user_one)
            assert result == expected


class TestUserResource:
    @patch.object(UserService, "get_all", fake_get_all)
    def test_get(self, client: FlaskClient):
        with client:
            # Test with no query parameters
            results = client.get(
                f"/api/{BASE_ROUTE}/users/", follow_redirects=True
            ).get_json()
            expected = UserPaginatedSchema().dump(
                fake_get_all(
                    page=USERS_DEFAULT_PAGE,
                    size=USERS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by=USERS_DEFAULT_SORT_FIELD,
                    direction=USERS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Change size
            results = client.get(
                f"/api/{BASE_ROUTE}/users/",
                query_string=dict(size=1),
                follow_redirects=True,
            ).get_json()
            expected = UserPaginatedSchema().dump(
                fake_get_all(
                    page=USERS_DEFAULT_PAGE,
                    size=1,
                    term=None,
                    sort_by=USERS_DEFAULT_SORT_FIELD,
                    direction=USERS_DEFAULT_SORT_DIRECTION,
                )
            )

            assert results == expected

            # Change page
            results = client.get(
                f"/api/{BASE_ROUTE}/users/",
                query_string=dict(page=2, size=1),
                follow_redirects=True,
            ).get_json()
            expected = UserPaginatedSchema().dump(
                fake_get_all(
                    page=2,
                    size=1,
                    term=None,
                    sort_by=USERS_DEFAULT_SORT_FIELD,
                    direction=USERS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Search
            results = client.get(
                f"/api/{BASE_ROUTE}/users/",
                query_string=dict(term="ohn"),
                follow_redirects=True,
            ).get_json()
            expected = UserPaginatedSchema().dump(
                fake_get_all(
                    page=USERS_DEFAULT_PAGE,
                    size=USERS_DEFAULT_PAGE_SIZE,
                    term="ohn",
                    sort_by=USERS_DEFAULT_SORT_FIELD,
                    direction=USERS_DEFAULT_SORT_DIRECTION,
                )
            )
            assert results == expected

            # Sort
            results = client.get(
                f"/api/{BASE_ROUTE}/users/",
                query_string=dict(sortBy="email", sortDirection="desc"),
                follow_redirects=True,
            ).get_json()
            expected = UserPaginatedSchema().dump(
                fake_get_all(
                    page=USERS_DEFAULT_PAGE,
                    size=USERS_DEFAULT_PAGE_SIZE,
                    term=None,
                    sort_by="email",
                    direction="desc",
                )
            )
            assert results == expected

    def fake_create(*args):
        return make_user(id=1)

    @patch.object(UserService, "create", fake_create)
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(
                uid=USER_ONE_UID,
                email=USER_ONE_EMAIL,
                first_name=USER_ONE_FIRST_NAME,
                last_name=USER_ONE_LAST_NAME,
                comment=USER_ONE_COMMENT,
                role=USER_ONE_ROLE,
                active=True,
                kind=UserKind.EMPLOYEE,
            )

            expected = UserSchema().dump(
                User(
                    id=1,
                    uid=payload["uid"],
                    email=payload["email"],
                    first_name=payload["first_name"],
                    last_name=payload["last_name"],
                    comment=payload["comment"],
                    role=payload["role"],
                    active=True,
                    kind=UserKind.EMPLOYEE,
                )
            )
            result = client.post(f"/api/{BASE_ROUTE}/users/", json=payload).get_json()
            assert result == expected


def fake_update(user: User, changes: UserInterface) -> User:
    # To fake an update, just return a new object
    updated_user = User(
        id=user.id,
        uid=changes["uid"],
        first_name=changes["first_name"],
        last_name=changes["last_name"],
        email=changes["email"],
        comment=changes["comment"],
        role=changes["role"],
        kind=UserKind.EMPLOYEE,
        active=True,
    )
    return updated_user


class TestUserIdResource:
    @patch.object(UserService, "get_by_id", lambda id: make_user(id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/users/123").get_json()
            expected = User(id=123)
            assert result["id"] == expected.id

    @patch.object(UserService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/users/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(UserService, "get_by_id", lambda id: make_user(id=id))
    @patch.object(UserService, "update", fake_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/users/123",
                json={
                    "uid": USER_ONE_UID,
                    "email": USER_ONE_EMAIL,
                    "first_name": USER_ONE_FIRST_NAME,
                    "last_name": USER_ONE_LAST_NAME,
                    "comment": USER_ONE_COMMENT,
                    "role": USER_ONE_ROLE,
                },
            ).get_json()
            expected = UserSchema().dump(
                User(
                    id=123,
                    uid=USER_ONE_UID,
                    email=USER_ONE_EMAIL,
                    first_name=USER_ONE_FIRST_NAME,
                    last_name=USER_ONE_LAST_NAME,
                    comment=USER_ONE_COMMENT,
                    role=USER_ONE_ROLE,
                    kind=UserKind.EMPLOYEE,
                    active=True,
                )
            )
            assert result == expected
