from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import and_

from app import db
from app.common.base_model import BaseMixin


class Ceiling(BaseMixin, db.Model):
    __tablename__ = "ceiling"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("ceilings", cascade="all, delete")
    )
    name = Column(String(255), nullable=True)
    known_U_value = Column(Boolean(), default=False, nullable=True)
    U_value = Column(Float(), nullable=True)
    composition = Column(String(255), nullable=True)
    insulated_wall = Column(Boolean(), default=False, nullable=True)
    known_insulation_value = Column(String(255), nullable=True)
    R_value = Column(Float(), nullable=True)
    insulation_thickness = Column(Integer(), nullable=True)
    insulation_type = Column(String(255), nullable=True)
    ceiling_position = Column(String(255), nullable=True)
    insulated_heated_non_heated_wall = Column(Boolean(), default=False, nullable=True)
    insulated_non_heated_exterior_wall = Column(Boolean(), default=False, nullable=True)
    type_non_heated_local = Column(String(255), nullable=True)

    @hybrid_property
    def total_surface(self):
        from app.perrenoud import Area, RoomInput, Room

        areas = Area.query.filter(
            Area.room_input.has(
                and_(
                    RoomInput.kind == "ceiling_inputs",
                    RoomInput.room.has(Room.scenario_id == self.scenario_id),
                )
            )
        ).all()

        result = 0
        for area in areas:
            if area.total:
                if area.total:
                    result += area.total
        return result

    @hybrid_property
    def surface(self):
        from app.perrenoud import Area, RoomInput, Room

        areas = Area.query.filter(
            Area.room_input.has(
                and_(
                    RoomInput.kind == "ceiling_inputs",
                    RoomInput.ceiling_id == self.id,
                    RoomInput.room.has(Room.scenario_id == self.scenario_id),
                )
            )
        ).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result
