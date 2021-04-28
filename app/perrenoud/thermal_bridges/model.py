from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class ThermalBridge(BaseMixin, db.Model):
    __tablename__ = "thermal_bridge"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("thermal_bridges", cascade="all, delete")
    )
    type = Column(String(255), nullable=True)
    length_m_liaison = Column(Float(), nullable=True)
    wall_name = Column(String(255), nullable=True)
    floor_name = Column(String(255), nullable=True)
    ceiling_name = Column(String(255), nullable=True)
    position_medium_floor = Column(String(255), nullable=True)
    position_shear_wall = Column(String(255), nullable=True)

    @hybrid_property
    def floor_id(self):
        from app.perrenoud.floors import Floor

        floor = (
            Floor.query.filter(Floor.scenario_id == self.scenario_id)
            .filter(Floor.name == self.floor_name)
            .first()
        )
        return floor.id if floor else None

    @hybrid_property
    def wall_id(self):
        from app.perrenoud.walls import Wall

        wall = (
            Wall.query.filter(Wall.scenario_id == self.scenario_id)
            .filter(Wall.name == self.wall_name)
            .first()
        )
        return wall.id if wall else None
