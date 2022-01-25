from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import and_, or_

from app import db
from app.common.base_model import BaseMixin


class Scenario(BaseMixin, db.Model):
    """Scenario"""

    __tablename__ = "scenario"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    is_initial_state = db.Column(Boolean, nullable=True, default=False)
    name = db.Column(String(255), nullable=True)
    annual_energy_consumption = db.Column(Float, nullable=True)
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship("Accommodation", backref="scenarios")
    energy_label = db.Column(String(255), nullable=True)
    energy_gain = db.Column(Integer(), nullable=True)
    annual_GES_emission = db.Column(Float(), nullable=True)
    GES_label = db.Column(String(255), nullable=True)
    loss_ceiling = db.Column(Integer(), nullable=True)
    loss_exterior_wall = db.Column(Integer(), nullable=True)
    loss_local_wall = db.Column(Integer(), nullable=True)
    loss_floor = db.Column(Integer(), nullable=True)
    loss_windows = db.Column(Integer(), nullable=True)
    loss_doors = db.Column(Integer(), nullable=True)
    loss_heat_bridges = db.Column(Integer(), nullable=True)
    loss_airflow = db.Column(Integer(), nullable=True)
    heat_energy_1_final = db.Column(Float(), nullable=True)
    heat_energy_1_primary = db.Column(Float(), nullable=True)
    heat_energy_2_final = db.Column(Float(), nullable=True)
    heat_energy_2_primary = db.Column(Float(), nullable=True)
    ECS_energy_1_final = db.Column(Float(), nullable=True)
    ECS_energy_1_primary = db.Column(Float(), nullable=True)
    ECS_energy_2_final = db.Column(Float(), nullable=True)
    ECS_energy_2_primary = db.Column(Float(), nullable=True)
    cooling_energy_1_final = db.Column(Float(), nullable=True)
    cooling_energy_1_primary = db.Column(Float(), nullable=True)
    cooling_energy_2_final = db.Column(Float(), nullable=True)
    cooling_energy_2_primary = db.Column(Float(), nullable=True)
    airflow_device = db.Column(String(255), nullable=True)
    air_conditioning_type = db.Column(String(255), nullable=True)
    air_conditioned_area = db.Column(Float(), nullable=True)
    has_photovoltaic_device = db.Column(Boolean, default=False, nullable=True)
    photovoltaic_device_surface = db.Column(Float(), nullable=True)
    inertia = db.Column(String(255), nullable=True)
    altitude = db.Column(String(255), nullable=True)
    commentary = Column(String(800), nullable=True)

    @hybrid_property
    def is_new(self):
        time_delta = self.updated_at - self.created_at
        return time_delta.seconds < 1

    @hybrid_property
    def recommendations_list(self):
        recommendation_list = []
        for recommendation in self.recommendations:
            if recommendation.heating_id:
                element_id = recommendation.heating_id
                table = "heating"
                name = recommendation.heating.heating_name
            elif recommendation.hot_water_id:
                element_id = recommendation.hot_water_id
                table = "hot_water"
                name = recommendation.hot_water.name
            else:
                element_id = recommendation.wall_id
                table = "wall"
                name = recommendation.wall.name

            recommendation_list.append(
                {
                    "recommendation": recommendation.recommendation,
                    "element": {
                        "name": name,
                        "element_id": element_id,
                        "table": table,
                    },
                }
            )
        return recommendation_list

    @hybrid_property
    def total_living_area(self):
        from app.perrenoud import Area, Room

        areas = Area.query.filter(Area.room.has(Room.scenario_id == self.id)).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result

    @hybrid_property
    def total_air_conditioned_area(self):
        from app.perrenoud import Area, Room

        areas = Area.query.filter(
            Area.room.has(
                and_(Room.scenario_id == self.id, Room.air_conditioning == True)
            )
        ).all()
        result = 0
        for area in areas:
            if area.total:
                result += area.total
        return result

    @hybrid_property
    def average_height_ceiling(self):
        from app.perrenoud import Room

        rooms = (
            Room.query.filter(Room.scenario_id == self.id)
            .filter(Room.height_under_ceiling != None)
            .all()
        )
        result = 0
        for room in rooms:
            result += room.height_under_ceiling
        return result

    @hybrid_property
    def wall_inputs(self):
        from app.perrenoud import Room, RoomInput
        from app.perrenoud.room_inputs.service import RoomInputKinds

        rooms_id = tuple([room.id for room in self.rooms])
        return (
            RoomInput.query.filter(RoomInput.kind == RoomInputKinds.WALL.value)
            .filter(RoomInput.room.has(Room.id.in_(rooms_id)))
            .all()
        )

    @hybrid_property
    def ceiling_inputs(self):
        from app.perrenoud import Room, RoomInput
        from app.perrenoud.room_inputs.service import RoomInputKinds

        rooms_id = tuple([room.id for room in self.rooms])
        return (
            RoomInput.query.filter(RoomInput.kind == RoomInputKinds.CEILING.value)
            .filter(RoomInput.room.has(Room.id.in_(rooms_id)))
            .all()
        )

    @hybrid_property
    def floor_inputs(self):
        from app.perrenoud import Room, RoomInput
        from app.perrenoud.room_inputs.service import RoomInputKinds

        rooms_id = tuple([room.id for room in self.rooms])
        return (
            RoomInput.query.filter(RoomInput.kind == RoomInputKinds.FLOOR.value)
            .filter(RoomInput.room.has(Room.id.in_(rooms_id)))
            .all()
        )

    @hybrid_property
    def doors(self):
        from app.perrenoud import Woodwork

        doors = (
            Woodwork.query.filter(Woodwork.scenario_id == self.id)
            .filter(Woodwork.type_election == "Porte")
            .all()
        )
        return doors if doors else []

    @hybrid_property
    def windows(self):
        from app.perrenoud import Woodwork

        windows = (
            Woodwork.query.filter(Woodwork.scenario_id == self.id)
            .filter(Woodwork.type_election == "Fenêtre")
            .all()
        )
        return windows
