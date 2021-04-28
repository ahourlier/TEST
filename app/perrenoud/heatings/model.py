from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import and_
from app import db
from app.common.base_model import BaseMixin


class Heating(BaseMixin, db.Model):
    __tablename__ = "heating"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("heatings", cascade="all, delete")
    )
    heating_name = Column(String(255), nullable=True)
    emissions_type = Column(String(255), nullable=True)
    energy_used = Column(String(255), nullable=True)
    generator_type = Column(String(255), nullable=True)
    is_power_known = db.Column(Boolean, default=False, nullable=True)
    power = db.Column(Integer(), nullable=True)
    has_regulation = db.Column(Boolean, default=False, nullable=True)
    wall_mounted_boiler = db.Column(Boolean, default=False, nullable=True)
    isolated_network = db.Column(Boolean, default=False, nullable=True)
    emettor_type = Column(String(255), nullable=True)
    installation_year = Column(String(255), nullable=True)
    intermittent_equipment = Column(String(255), nullable=True)
    wood_oven = db.Column(Boolean, default=False, nullable=True)
    equipment_performance = Column(String(255), nullable=True)
    heated_area = db.Column(Float(), nullable=True)
    known_caracteristics = db.Column(Boolean, default=False, nullable=True)
    full_yield = db.Column(Float(), nullable=True)
    middle_yield = db.Column(Float(), nullable=True)
    COP = db.Column(Float(), nullable=True)

    @hybrid_property
    def heated_area(self):
        from app.perrenoud import Area, Room

        areas = Area.query.filter(
            Area.room.has(
                and_(Room.scenario_id == self.scenario_id, Room.heating_id == self.id)
            )
        ).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result
