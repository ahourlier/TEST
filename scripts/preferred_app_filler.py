import sys
import os
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

from app import create_app, db
from app.auth.preferred_app import PreferredApp
from app.auth.users import User
from app.common.app_name import App

app = create_app("dev")

def fill_preferred_app():
    with app.app_context():
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

fill_preferred_app()