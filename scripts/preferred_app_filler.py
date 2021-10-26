from app import db, create_app
from app.auth.preferred_app import PreferredApp
from app.auth.preferred_app.model import App
from app.auth.users import User


def fill_preferred_app():
    users = User.query.all()
    for u in users:
        if not u.preferred_app_id:
            print(f"{u.email} has no preferred app")
            preferred_app = PreferredApp(
                **{"preferred_app": App.INDIVIDUAL, "first_connection": False}
            )
            db.session.add(preferred_app)
            db.session.commit()
            u.preferred_app_id = preferred_app.id
            db.session.commit()
