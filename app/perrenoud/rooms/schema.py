from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields
from app.perrenoud.heatings.schema import HeatingSchema
from app.perrenoud.room_inputs.schema import RoomInputSchema
from app.perrenoud.rooms import Room
from app.perrenoud.areas.schema import AreaSchema


class RoomSchema(SQLAlchemyAutoSchema):
    areas = fields.List(fields.Nested(AreaSchema(), allow_none=True, required=False))
    heating = fields.Nested(HeatingSchema(), allow_none=True, required=False)
    wall_inputs = fields.List(fields.Nested(RoomInputSchema(), required=False))
    woodwork_inputs = fields.List(fields.Nested(RoomInputSchema(), required=False))
    ceiling_inputs = fields.List(fields.Nested(RoomInputSchema(), required=False))
    floor_inputs = fields.List(fields.Nested(RoomInputSchema(), required=False))
    thermal_bridge_inputs = fields.List(
        fields.Nested(RoomInputSchema(), required=False)
    )

    class Meta:
        model = Room
        include_fk = True
        unknown = EXCLUDE


class RoomPaginatedSchema(SQLAlchemyAutoSchema):
    items = fields.Nested(RoomSchema(), many=True, dump_only=True)
