from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class Disorder(BaseMixin, db.Model):
    """ Disorder  """

    __tablename__ = "disorder"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    priority = Column(Integer(), nullable=True)
    analysis_localisation = Column(String(255), nullable=True)
    analysis_comment = Column(String(2083), nullable=True)
    recommendation_localisation = Column(String(255), nullable=True)
    recommendation_comment = Column(String(2083), nullable=True)
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship(
        "Accommodation", backref=backref("disorders", cascade="all, delete-orphan")
    )
    common_area_id = Column(Integer, ForeignKey("common_area.id"), nullable=True)
    common_area = relationship(
        "CommonArea", backref=backref("disorders", cascade="all, delete-orphan")
    )

    @hybrid_property
    def analysis_types(self):
        return [t for t in self.disorder_types if t.is_analysis]

    @hybrid_property
    def recommendation_types(self):
        return [t for t in self.disorder_types if not t.is_analysis]


class DisorderType(BaseMixin, db.Model):
    """ Disorder type """

    __tablename__ = "disorder_type"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type_name = Column(String(255), nullable=False)
    is_analysis = Column(Boolean, nullable=False)
    disorder_id = Column(Integer, ForeignKey("disorder.id"), nullable=False)
    disorder = relationship(
        "Disorder", backref=backref("disorder_types", cascade="all, delete-orphan")
    )
