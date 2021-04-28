from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.perrenoud.areas.schema import AreaSchema
from app.perrenoud.ceilings.schema import CeilingSchema
from app.perrenoud.floors.schema import FloorSchema
from app.perrenoud.room_inputs import RoomInput
from app.perrenoud.walls.schema import WallSchema
from app.perrenoud.woodworks.schema import WoodworkSchema


class RoomInputSchema(SQLAlchemyAutoSchema):
    areas = fields.List(fields.Nested(AreaSchema()))
    wall = fields.Nested(WallSchema(), allow_none=True, dump_only=True, required=False)
    woodwork = fields.Nested(
        WoodworkSchema(), allow_none=True, dump_only=True, required=False
    )
    ceiling = fields.Nested(
        CeilingSchema(), allow_none=True, dump_only=True, required=False
    )
    floor = fields.Nested(
        FloorSchema(), allow_none=True, dump_only=True, required=False
    )

    class Meta:
        model = RoomInput
        include_fk = True
        unknown = EXCLUDE
