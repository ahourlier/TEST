from flask import g
from functools import wraps
from unittest.mock import patch

import pytest

from app import create_app


def mock_auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.auth.users.model_test import create_user_one

        g.user = create_user_one()
        return func(*args, **kwargs)

    return wrapper


@pytest.fixture
def app():
    patch("app.common.decorators.auth_required", mock_auth_decorator).start()
    return create_app("test")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app import db

    with app.app_context():
        db.engine.execute("ATTACH ':memory:' AS core")
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
