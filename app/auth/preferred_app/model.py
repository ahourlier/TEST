from sqlalchemy import Column, String, Boolean, Integer

from app import db
from app.common.base_model import BaseMixin


class App:
    COPRO = "COPROPRIETE"
    INDIVIDUAL = "INDIVIDUEL"


class PreferredApp(BaseMixin, db.Model):
    """ Application User """

    __tablename__ = "preferred_app"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    preferred_app = Column(String(11))
    first_connection = Column(Boolean(), nullable=False)


