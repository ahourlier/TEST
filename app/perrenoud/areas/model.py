from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class Area(BaseMixin, db.Model):
    __tablename__ = "area"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=True)
    room = relationship(
        "Room", backref=backref("areas", cascade="all, delete", uselist=True)
    )
    room_input_id = Column(Integer, ForeignKey("room_input.id"), nullable=True)
    room_input = relationship(
        "RoomInput", backref=backref("areas", cascade="all, delete")
    )
    length = Column(Float(), nullable=True)
    width = Column(Float(), nullable=True)
    height = Column(Float(), nullable=True)
    total = Column(Float(), nullable=True)
    wall_id = Column(Integer, ForeignKey("wall.id"), nullable=True)
    wall = relationship("Wall", backref=backref("areas", cascade="all, delete"))
    ceiling_id = Column(Integer, ForeignKey("ceiling.id"), nullable=True)
    ceiling = relationship("Ceiling", backref=backref("areas", cascade="all, delete"))
    number_identical_woodwork = Column(Integer(), nullable=True)

    @hybrid_property
    def perimeter(self):
        perimeter = 0
        valid_sizes = 0
        if self.length:
            perimeter += self.length * 2
            valid_sizes += 1
        if self.width:
            perimeter += self.width * 2
            valid_sizes += 1
        if self.height:
            perimeter += self.height * 2
            valid_sizes += 1
        if valid_sizes != 2:
            return None
        return perimeter

    @hybrid_property
    def surface_woodworks(self):
        if self.total:
            return (
                self.number_identical_woodwork * self.total
                if self.number_identical_woodwork
                else self.total
            )
        return None

    @hybrid_property
    def woodwork_id(self):
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if (
            self.room_input.kind == RoomInputKinds.WOODWORK.value
            and self.room_input.woodwork_id
        ):
            return self.room_input.woodwork_id
        return None
