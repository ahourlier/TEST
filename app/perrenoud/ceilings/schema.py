from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields
from app.perrenoud.ceilings import Ceiling


class CeilingSchema(SQLAlchemyAutoSchema):
    total_surface = fields.Float(dump_only=True, required=False)
    surface = fields.Float(dump_only=True, required=False)

    class Meta:
        model = Ceiling
        include_k = True
        unknown = EXCLUDE
