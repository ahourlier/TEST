import os
import psutil
import tracemalloc
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify, g
from flask_admin import Admin
from flask_allows import Allows
from flask_babelex import Babel

from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

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
migrate = Migrate()
co = CORS()
allows = Allows()
babel = Babel()

process = psutil.Process(os.getpid())
tracemalloc.start()
s = None


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.admin_setup import register_admin_views

    from app.internal_api import internal_api_blueprint, register_internal_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or os.getenv("FLASK_ENV") or "test"])
    app.secret_key = os.getenv("SECRET_KEY")
    api = Api(app, title="OSLO API", version="1.0.0")
    print(f"Current env is {app.config['CONFIG_NAME']}")
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    co.init_app(app)
    allows.init_app(app)
    allows.identity_loader(lambda: g.user)
    babel.init_app(app)
    if env != "test":
        creds = credentials.Certificate(
            app.config.get("FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY_PATH")
        )
        firebase_admin.initialize_app(creds)
    fa = Admin(name="OSLO", template_mode="bootstrap3", url="/_/manage")
    fa.init_app(app)

    internal_bp = internal_api_blueprint()

    register_admin_views(fa, db)
    register_routes(api, app)
    register_internal_routes(internal_bp)
    app.register_blueprint(internal_bp)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.route("/_ah/warmup")
    def warmup():
        # Handle warmup
        return "", 200, {}

    @app.route("/memory")
    def print_memory():
        return {"memory": process.memory_info().rss}

    @app.route("/snapshot")
    def snap():
        global s
        if not s:
            s = tracemalloc.take_snapshot()
            return "taken snapshot\n"
        else:
            lines = []
            top_stats = tracemalloc.take_snapshot().compare_to(s, "lineno")
            for stat in top_stats[:5]:
                lines.append(str(stat))
            return "\n".join(lines)

    return app
