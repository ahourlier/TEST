from app.auth.preferred_app.interface import PreferredAppInterface
from app.auth.preferred_app.service import PreferredAppService
from app.common.app_name import App
from tests.conftest import create_app, db
from app.auth.preferred_app.model import PreferredApp


def test_create_preferred_app():
    app = create_app()
    with app.app_context():

        db_pa = PreferredApp.query.first()
        assert db_pa is None
        preferred_app = PreferredAppInterface()
        preferred_app.preferred_app = App.INDIVIDUAL
        preferred_app.first_connection = True
        PreferredAppService.create(preferred_app)
        db_pa = PreferredApp.query.first()
        assert db_pa is not None

