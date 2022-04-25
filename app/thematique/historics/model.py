from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin


class Historic(SoftDeletableMixin, BaseMixin, db.Model):
    """Represents a historic"""

    __tablename__ = "historic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(String, nullable=False)
    updated_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_by = relationship("User", backref="historics")
    step_name = Column(String, nullable=False)
    status_changed = Column(Boolean, nullable=False)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)
