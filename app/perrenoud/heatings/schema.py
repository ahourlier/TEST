from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.perrenoud.heatings import Heating


class HeatingSchema(SQLAlchemyAutoSchema):
    heated_area = fields.Float(dump_only=True, required=False)

    class Meta:
        model = Heating
        include_fk = True
        unknown = EXCLUDE
