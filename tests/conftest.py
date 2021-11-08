from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, inspect

metadata = MetaData(schema="core")
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()


def create_app():
    """Create flask app"""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.engine.execute("ATTACH ':memory:' AS core")
        db.create_all(app=app)

        inspector = inspect(db.engine)
        print("tables")
        print(inspector.get_table_names(schema="core"))

    return app

