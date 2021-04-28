from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.elements import and_

from app import db
from app.common.base_model import BaseMixin


class Woodwork(BaseMixin, db.Model):
    __tablename__ = "woodwork"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    scenario = relationship(
        "Scenario", backref=backref("woodworks", cascade="all, delete")
    )
    door_name = Column(String(255), nullable=True)
    windows_name = Column(String(255), nullable=True)
    type_election = Column(String(255), nullable=True)
    woodwork_known_U_value = Column(Boolean(), default=False, nullable=True)
    woodwork_U_value = Column(Float(), nullable=True)
    door_nature = Column(String(255), nullable=True)
    door_type = Column(String(255), nullable=True)
    door_known_U_value = Column(Boolean(), default=False, nullable=True)
    door_U_value = Column(Float(), nullable=True)
    Ujn_value = Column(Float(), nullable=True)
    glass_wall_type = Column(String(255), nullable=True)
    windows_type = Column(String(255), nullable=True)
    materials = Column(String(255), nullable=True)
    glass_type = Column(String(255), nullable=True)
    glass_insulated = Column(Boolean(), default=False, nullable=True)
    argon_krypton_filling = Column(Boolean(), default=False, nullable=True)
    thickness_air_gap = Column(Integer(), nullable=True)
    closing_type = Column(String(255), nullable=True)
    inclination = Column(String(255), default="0", nullable=True)

    @hybrid_property
    def total_surface(self):
        from app.perrenoud import Area, RoomInput, Room

        areas = Area.query.filter(
            Area.room_input.has(
                and_(
                    RoomInput.kind == "woodwork_inputs",
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
                    RoomInput.kind == "woodwork_inputs",
                    RoomInput.woodwork_id == self.id,
                    RoomInput.room.has(Room.scenario_id == self.scenario_id),
                )
            )
        ).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result
