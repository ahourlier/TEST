from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from app import db
from app.common.base_model import BaseMixin


class Room(BaseMixin, db.Model):
    """Room"""

    __tablename__ = "room"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = db.Column(String(255), nullable=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario",
        backref=backref("rooms", cascade="all, delete", order_by="asc(Room.id)"),
    )
    heating_id = Column(Integer, ForeignKey("heating.id"), nullable=True)
    heating = relationship("Heating", backref=backref("rooms"))
    height_under_ceiling = db.Column(Float(), nullable=True)
    air_conditioning = db.Column(Boolean, default=False, nullable=True)

    @hybrid_property
    def wall_inputs(self):
        result = []
        for room_input in self.inputs:
            if room_input.kind == "wall_inputs":
                result.append(room_input)
        return result

    @hybrid_property
    def woodwork_inputs(self):
        result = []
        for room_input in self.inputs:
            if room_input.kind == "woodwork_inputs":
                result.append(room_input)
        return result

    @hybrid_property
    def ceiling_inputs(self):
        result = []
        for room_input in self.inputs:
            if room_input.kind == "ceiling_inputs":
                result.append(room_input)
        return result

    @hybrid_property
    def floor_inputs(self):
        result = []
        for room_input in self.inputs:
            if room_input.kind == "floor_inputs":
                result.append(room_input)
        return result
