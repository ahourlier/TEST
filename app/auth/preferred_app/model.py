from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin

# Do not remove, used for relationships
from app.auth.users import User


class App:
    COPRO = "COPROPRIETE"
    INDIVIDUAL = "INDIVIDUEL"


class PreferredApp(BaseMixin, db.Model):
    """ Application User """

    __tablename__ = "preferred_app"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    preferred_app = Column(String(11))
    first_connection = Column(Boolean(), nullable=False)
    user = relationship("User")


