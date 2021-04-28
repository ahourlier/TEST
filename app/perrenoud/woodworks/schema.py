from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.perrenoud.woodworks.model import Woodwork


class WoodworkSchema(SQLAlchemyAutoSchema):
    total_surface = fields.Float(dump_only=True, required=False)
    surface = fields.Float(dump_only=True, required=False)

    class Meta:
        model = Woodwork
        include_fk = True
        unknown = EXCLUDE
