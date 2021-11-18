from flask_sqlalchemy import SQLAlchemy
from app.test.fixtures import app, db
from .interface import PreferredAppInterface
from .model import PreferredApp
from .service import PreferredAppService
from ...common.app_name import App

mock_preferred_app = PreferredAppInterface(**{
    "preferred_app": App.INDIVIDUAL,
    "first_connection": True
})


def test_create(db: SQLAlchemy):
    preferred_apps = PreferredApp.query.all()
    assert len(preferred_apps) == 0
    res = PreferredAppService.create(mock_preferred_app)
    preferred_app = PreferredApp.query.first()
    assert preferred_app is not None
    assert preferred_app.preferred_app == mock_preferred_app.get("preferred_app")
    assert preferred_app.first_connection == mock_preferred_app.get("first_connection")

