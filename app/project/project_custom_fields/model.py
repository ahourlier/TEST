from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import SoftDeletableMixin, BaseMixin
from app.mission.custom_fields import CustomField  # To keep.


class ProjectCustomField(SoftDeletableMixin, BaseMixin, db.Model):
    """ ProjectCustomField  """

    __tablename__ = "project_custom_field"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    value = Column(String(800), nullable=True)
    custom_field_id = Column(Integer, ForeignKey("custom_field.id"), nullable=True)
    custom_field = relationship("CustomField", backref="project_custom_fields")
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship("Project", backref="custom_fields")


class CustomFieldValue(SoftDeletableMixin, BaseMixin, db.Model):
    """ CustomFieldValue  """

    __tablename__ = "custom_field_value"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    value = Column(String(800), nullable=True)
    project_custom_field_id = Column(
        Integer, ForeignKey("project_custom_field.id"), nullable=True
    )
    project_custom_field = relationship(
        "ProjectCustomField",
        backref=backref("multiple_values", cascade="all, delete-orphan"),
    )
