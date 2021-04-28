from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import and_

from app import db
from app.common.base_model import BaseMixin


class Floor(BaseMixin, db.Model):
    __tablename__ = "floor"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("floors", cascade="all, delete")
    )
    name = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    perimeter = db.Column(Float(), nullable=True)
    insulated_heated_non_heated_wall = db.Column(Boolean, default=False, nullable=True)
    insulated_non_heated_exterior_wall = db.Column(
        Boolean, default=False, nullable=True
    )
    type_non_heated_local = Column(String(255), nullable=True)
    known_U_value = db.Column(Boolean, default=False, nullable=True)
    U_value = db.Column(Float(), nullable=True)
    main_component = Column(String(255), nullable=True)
    insulated_wall = db.Column(Boolean, default=False, nullable=True)
    known_insulation_value = Column(String(255), nullable=True)
    R_value = db.Column(Float(), nullable=True)
    insulation_thickness = db.Column(Integer(), nullable=True)
    insulation_type = Column(String(255), nullable=True)

    @hybrid_property
    def total_surface(self):
        from app.perrenoud import Area, RoomInput, Room

        areas = Area.query.filter(
            Area.room_input.has(
                and_(
                    RoomInput.kind == "floor_inputs",
                    RoomInput.room.has(Room.scenario_id == self.scenario_id),
                )
            )
        ).all()

        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result

    @hybrid_property
    def surface(self):
        from app.perrenoud import Area, RoomInput, Room

        areas = Area.query.filter(
            Area.room_input.has(
                and_(
                    RoomInput.kind == "floor_inputs",
                    RoomInput.floor_id == self.id,
                    RoomInput.room.has(Room.scenario_id == self.scenario_id),
                )
            )
        ).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result
