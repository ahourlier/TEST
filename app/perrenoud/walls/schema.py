from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.perrenoud.walls.model import Wall


class WallSchema(SQLAlchemyAutoSchema):
    total_surface = fields.Float(dump_only=True, required=False)
    surface = fields.Float(dump_only=True, required=False)

    class Meta:
        model = Wall
        include_fk = True
        unknown = EXCLUDE
