from unittest.mock import patch

from flask_sqlalchemy import SQLAlchemy
from flask import g

from app.auth.users import User
from app.auth.users.interface import UserInterface
from app.auth.users.model_test import USER_ONE_EMAIL, USER_ONE_UID, create_user_one
from app.auth.users.service import UserService
from app.test.fixtures import app, db
from app.common.decorators import auth_required
import google.oauth2.id_token


USER_ONE_FIREBASE_TOKEN = {
    "iss": "https://securetoken.google.com/myapp",
    "aud": "myapp",
    "user_id": USER_ONE_UID,
    "sub": USER_ONE_UID,
    "email": USER_ONE_EMAIL,
    "email_verified": False,
    "firebase": {
        "identities": {"email": [USER_ONE_EMAIL]},
        "sign_in_provider": "password",
    },
}


def func():
    return "OK", 200


def test_auth_required_not_authenticated(app):
    with app.test_request_context():
        decorated_func = auth_required(func)
        resp, status = decorated_func()
        assert status == 401


def fake_check_auth_informations(
    email: str, changes: UserInterface, force_update: bool = False
) -> User:
    return create_user_one()


def test_auth_required_authenticated(app, db: SQLAlchemy):
    with app.test_request_context(headers={"Authorization": "Bearer abcdef"}):
        with patch.object(
            google.oauth2.id_token,
            "verify_firebase_token",
            return_value=USER_ONE_FIREBASE_TOKEN,
        ):
            with patch.object(
                UserService, "check_auth_informations", fake_check_auth_informations
            ):
                # create user en user_one
                decorated_func = auth_required(func)
                resp, status = decorated_func()
                assert status == 200
                assert resp == "OK"
                assert g.user is not None
                assert g.user.email == USER_ONE_EMAIL
