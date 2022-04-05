from sqlalchemy import Column, Integer, String, JSON

from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin


class Historic(SoftDeletableMixin, BaseMixin, db.Model):
    """Represents a historic"""

    __tablename__ = "historic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    thematique_id = Column(String, nullable=False)
    old_value = Column(JSON, nullable=False)
    new_value = Column(JSON, nullable=False)
