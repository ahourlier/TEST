from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class Recommendation(BaseMixin, db.Model):
    """ Disorder  """

    __tablename__ = "recommendation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    recommendation = Column(String(255), nullable=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("recommendations", cascade="all, delete-orphan")
    )
    heating_id = Column(Integer, ForeignKey("heating.id"), nullable=True)
    heating = relationship("Heating", backref=backref("recommendations"))
    hot_water_id = Column(Integer, ForeignKey("hot_water.id"), nullable=True)
    hot_water = relationship("HotWater", backref=backref("recommendations"))
    wall_id = Column(Integer, ForeignKey("wall.id"), nullable=True)
    wall = relationship("Wall", backref=backref("recommendations"))
