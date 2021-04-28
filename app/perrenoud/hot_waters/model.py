from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db
from app.common.base_model import BaseMixin


class HotWater(BaseMixin, db.Model):
    __tablename__ = "hot_water"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("hot_waters", cascade="all, delete")
    )
    name = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    boiler_type = Column(String(255), nullable=True)
    year_classic_accumulator = Column(String(255), nullable=True)
    has_light = Column(Boolean(), default=False, nullable=True)
    production_living_volume = Column(String(255), nullable=True)
    linked_rooms = Column(Boolean(), default=False, nullable=True)
    production_type = Column(String(255), nullable=True)
    water_tank_volume = Column(Integer(), nullable=True)
    renovated_production = Column(Boolean(), default=False, nullable=True)
    existing_solar_device = Column(Boolean(), default=False, nullable=True)
    solar_device_type = Column(String(255), nullable=True)
