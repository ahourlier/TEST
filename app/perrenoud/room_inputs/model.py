from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from app import db
from app.common.base_model import BaseMixin


class RoomInput(BaseMixin, db.Model):
    __tablename__ = "room_input"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    kind = Column(String(255), nullable=True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=True)
    room = relationship("Room", backref=backref("inputs", cascade="all, delete"))
    wall_id = Column(Integer, ForeignKey("wall.id"), nullable=True)
    wall = relationship("Wall", backref=backref("inputs", cascade="all, delete"))
    woodwork_id = Column(Integer, ForeignKey("woodwork.id"), nullable=True)
    woodwork = relationship(
        "Woodwork", backref=backref("inputs", cascade="all, delete")
    )
    ceiling_id = Column(Integer, ForeignKey("ceiling.id"), nullable=True)
    ceiling = relationship("Ceiling", backref=backref("inputs", cascade="all, delete"))
    floor_id = Column(Integer, ForeignKey("floor.id"), nullable=True)
    floor = relationship("Floor", backref=backref("inputs", cascade="all, delete"))

    @hybrid_property
    def surface(self):

        total = 0
        for area in self.areas:
            if area.total:
                total += area.total
        return total

    @hybrid_property
    def linked_areas_woodworks(self):
        from app.perrenoud.areas import Area
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if self.kind == RoomInputKinds.WALL.value:
            return (
                Area.query.filter(Area.wall_id == self.wall_id)
                .filter(Area.room_input.has(RoomInput.room_id == self.room_id))
                .all()
            )
        if self.kind is RoomInputKinds.CEILING.value:
            return (
                Area.query.filter(Area.ceiling_id == self.ceiling_id)
                .filter(Area.room_input.has(RoomInput.room_id == self.room_id))
                .all()
            )
        return []

    @hybrid_property
    def linked_areas_number_identicals(self):
        total_number_identicals = 0
        for area in self.linked_areas_woodworks:
            if area.number_identical_woodwork:
                total_number_identicals += area.number_identical_woodwork
        return total_number_identicals

    @hybrid_property
    def linked_areas_woodworks_surface(self):
        total_surface = 0
        for area in self.linked_areas_woodworks:
            if area.surface_woodworks:
                total_surface += area.surface_woodworks
        return total_surface

    @hybrid_property
    def low_thermal_bridges(self):
        from app.perrenoud.thermal_bridges import ThermalBridge
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if self.kind == RoomInputKinds.FLOOR.value:
            return (
                ThermalBridge.query.filter(
                    ThermalBridge.scenario_id == self.room.scenario_id
                )
                .filter(ThermalBridge.floor_name == self.floor.name)
                .filter(ThermalBridge.type == "Mur ext / Plancher bas")
                .all()
            )

        return []

    @hybrid_property
    def middle_thermal_bridges(self):
        from app.perrenoud.thermal_bridges import ThermalBridge
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if self.kind == RoomInputKinds.FLOOR.value:
            return (
                ThermalBridge.query.filter(
                    ThermalBridge.scenario_id == self.room.scenario_id
                )
                .filter(ThermalBridge.floor_name == self.floor.name)
                .filter(ThermalBridge.type == "Mur ext / Plancher intermédiaire")
                .all()
            )

        return []

    @hybrid_property
    def high_thermal_bridges(self):
        from app.perrenoud.thermal_bridges import ThermalBridge
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if self.kind == RoomInputKinds.FLOOR.value:
            return (
                ThermalBridge.query.filter(
                    ThermalBridge.scenario_id == self.room.scenario_id
                )
                .filter(ThermalBridge.floor_name == self.floor.name)
                .filter(ThermalBridge.type == "Mur ext / Plafond")
                .all()
            )

        return []

    @hybrid_property
    def refend_thermal_bridges(self):
        from app.perrenoud.thermal_bridges import ThermalBridge
        from app.perrenoud.room_inputs.service import RoomInputKinds

        if self.kind == RoomInputKinds.FLOOR.value:
            return (
                ThermalBridge.query.filter(
                    ThermalBridge.scenario_id == self.room.scenario_id
                )
                .filter(ThermalBridge.floor_name == self.floor.name)
                .filter(ThermalBridge.type == "Mur ext / Refend")
                .all()
            )

        return []
