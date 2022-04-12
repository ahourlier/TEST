from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import SoftDeletableMixin, BaseMixin


class FieldsCategories(Enum):
    REQUESTER = "requester"
    FUNDERS = "funders"
    ACCOMMODATION = "accommodation"


class CustomField(SoftDeletableMixin, BaseMixin, db.Model):
    """CustomField"""

    __tablename__ = "custom_field"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    category = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    is_multiple = Column(Boolean(255), nullable=True, default=False)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=True)
    mission = relationship("Mission", backref="custom_fields")


class AvailableFieldValue(SoftDeletableMixin, BaseMixin, db.Model):
    """AvailableFieldValue"""

    __tablename__ = "available_field_value"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    value = Column(String(800), nullable=True)
    custom_field_id = Column(Integer, ForeignKey("custom_field.id"), nullable=True)
    custom_field = relationship(
        "CustomField",
        backref=backref("available_values", cascade="all, delete-orphan"),
    )
