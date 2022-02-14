from sqlalchemy import Column, Integer, Text, String, select, ForeignKey, Table, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db, metadata
from app.common.base_model import BaseMixin, SoftDeletableMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Task(SoftDeletableMixin, BaseMixin, db.Model):
    """Represents a task"""

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(Text())
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship(
        "User",
        foreign_keys=[author_id],
        backref=backref("created_tasks", cascade="all, delete"),
    )
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    assignee = relationship(
        "User",
        foreign_keys=[assignee_id],
        backref=backref("assigned_tasks", cascade="all, delete"),
    )
    status = Column(String(255))
    step_id = Column(String(255))
    version_id = Column(String(255))
    reminder_date = db.Column(db.Date, nullable=True)
    date = db.Column(db.Date, nullable=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=True)
    mission = relationship("Mission", backref=backref("tasks", cascade="all, delete"))