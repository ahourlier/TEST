from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields, Schema
from app.perrenoud.scenarios import Scenario
from app.project.simulations.schema import SimulationSchema
from app.perrenoud.ceilings.schema import CeilingSchema
from app.perrenoud.floors.schema import FloorSchema
from app.perrenoud.heatings.schema import HeatingSchema
from app.perrenoud.hot_waters.schema import HotWaterSchema
from app.perrenoud.recommendations.schema import RecommendationSchema
from app.perrenoud.thermal_bridges.schema import ThermalBridgeSchema
from app.perrenoud.walls.schema import WallSchema
from app.perrenoud.woodworks.schema import WoodworkSchema
from app.perrenoud.rooms.schema import RoomSchema


class ScenarioSchema(SQLAlchemyAutoSchema):
    heatings = fields.List(fields.Nested(HeatingSchema()), required=False)
    hot_waters = fields.List(fields.Nested(HotWaterSchema()), required=False)
    walls = fields.List(fields.Nested(WallSchema()), required=False)
    woodworks = fields.List(fields.Nested(WoodworkSchema()), required=False)
    ceilings = fields.List(fields.Nested(CeilingSchema()), required=False)
    floors = fields.List(fields.Nested(FloorSchema()), required=False)
    thermal_bridges = fields.List(fields.Nested(ThermalBridgeSchema()), required=False)
    rooms = fields.List(fields.Nested(RoomSchema()), required=False)
    total_living_area = fields.Float(dump_only=True, required=False)
    average_height_ceiling = fields.Float(dump_only=True, required=False)
    accommodation_id = fields.Integer(required=True)
    recommendations_list = fields.List(fields.Nested(RecommendationSchema()))
    is_new = fields.Boolean(dump_only=True)
    simulations = fields.List(fields.Nested(SimulationSchema()), dump_only=True)

    class Meta:
        model = Scenario
        include_fk = True
        unknown = EXCLUDE


class PerrenoudAnalysisErrors(Schema):
    error_type = fields.String()
    xml_id = fields.Integer()
    tag_name = fields.String()
    entity_name = fields.String()
    entity_id = fields.Integer()


class ScenarioPaginatedSchema(SQLAlchemyAutoSchema):
    items = fields.Nested(ScenarioSchema(), many=True, dump_only=True)
