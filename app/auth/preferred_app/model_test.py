# from flask_sqlalchemy import SQLAlchemy
# from pytest import fixture
#
# from .model import User, App, PreferredApp
#
# PREFERRED_APP_ONE_PREFERRED_APP = App.INDIVIDUAL
# PREFERRED_APP_ONE_FIRST_CONNECTION = True
#
# PREFERRED_APP_TWO_PREFERRED_APP = App.COPRO
# PREFERRED_APP_TWO_FIRST_CONNECTION = False
#
#
# def create_preferred_app_one() -> PreferredApp:
#     return PreferredApp(
#         id=1,
#         preferred_app=PREFERRED_APP_ONE_PREFERRED_APP,
#         first_connection=PREFERRED_APP_ONE_FIRST_CONNECTION
#     )
#
#
# def create_preferred_app_two() -> PreferredApp:
#     return PreferredApp(
#         id=2,
#         preferred_app=PREFERRED_APP_TWO_PREFERRED_APP,
#         first_connection=PREFERRED_APP_TWO_FIRST_CONNECTION
#     )
#
#
# @fixture
# def preferred_app() -> PreferredApp:
#     return create_preferred_app_one()
#
#
# def test_preferred_app_create(preferred_app: PreferredApp):
#     assert preferred_app
#
#
# def test_preferred_app_retrieve(preferred_app: PreferredApp, db: SQLAlchemy):
#     db.session.add(preferred_app)
#     db.session.commit()
#     s = PreferredApp.query.first()
#     assert s.__dict__ == preferred_app.__dict__
#
#
# def test_preferred_app_update(preferred_app: PreferredApp, db: SQLAlchemy):
#     db.session.add(preferred_app)
#     db.session.commit()
#     preferred_app.preferred_app = App.COPRO
#     db.session.add(preferred_app)
#     db.session.commit()
#
#     assert preferred_app.preferred_app == App.COPRO
#     assert preferred_app.updated_at is not None
