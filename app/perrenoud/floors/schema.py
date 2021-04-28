from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields
from app.perrenoud.floors import Floor


class FloorSchema(SQLAlchemyAutoSchema):
    total_surface = fields.Float(dump_only=True, required=False)
    surface = fields.Float(dump_only=True, required=False)

    class Meta:
        model = Floor
        include_fk = True
        unknown = EXCLUDE
