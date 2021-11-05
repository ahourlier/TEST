from flask import Flask, jsonify, g
from flask_marshmallow import Marshmallow

from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from app.auth.preferred_app.interface import PreferredAppInterface
from app.auth.preferred_app.service import PreferredAppService
from app.common.app_name import App
from app.config import config_by_name
# from app.routes import register_routes



convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    # https://github.com/sqlalchemy/sqlalchemy/issues/4784
    # https://github.com/sqlalchemy/sqlalchemy/issues/3345
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(schema="core", naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
app = Flask(__name__)
app.config.from_object(config_by_name["test"])
db.init_app(app)
ma.init_app(app)
api = Api(app, title="OSLO API", version="1.0.0")
# register_routes(api, app)


def test_create_preferred_app():
    with app.app_context():
        from app.auth.preferred_app.model import PreferredApp

        db.engine.execute("ATTACH ':memory:' AS core")
        db.drop_all()
        db.create_all()
        db.drop_all()
        db.session.commit()

        db_pa = PreferredApp.query.first()
        assert db_pa is None
        preferred_app = PreferredAppInterface()
        preferred_app.preferred_app = App.INDIVIDUAL
        preferred_app.first_connection = True
        PreferredAppService.create(preferred_app)
        db_pa = PreferredApp.query.first()
        assert db_pa is not None

