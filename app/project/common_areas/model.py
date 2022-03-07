from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class CommonArea(BaseMixin, db.Model):
    """Common Area"""

    __tablename__ = "common_area"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    condominium = Column(Boolean, nullable=True)
    purchase_year = Column(Integer(), nullable=True)
    construction_year = Column(Integer(), nullable=True)
    levels_nb = Column(Integer, nullable=True)
    commentary = Column(String(800), nullable=True)
    accommodations_nb = Column(Integer, nullable=True)
    area = Column(Float, nullable=True)
    degradation_coefficient = Column(Float, nullable=True)
    unsanitary_coefficient = Column(Float, nullable=True)
    note = Column(String(800), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    project = relationship(
        "Project", backref=backref("common_areas", cascade="all, delete", uselist=False)
    )
