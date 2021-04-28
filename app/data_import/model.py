from enum import Enum

from sqlalchemy import Column, Integer, String, Text

from app import db
from app.common.base_model import BaseMixin


class DataImportStatus(Enum):
    ON_GOING = "En cours"
    DONE = "Créé"
    ERROR = "Erreur"


class DataImport(BaseMixin, db.Model):
    """DataImport"""

    id = Column(Integer(), primary_key=True, autoincrement=True)
    status = Column(String(255), nullable=True)
    user_email = Column(String(255), nullable=True)
    data = Column(Text(), nullable=True)
    labels = Column(Text(), nullable=True)
