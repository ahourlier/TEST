from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Antenna
from ...common.schemas import PaginatedSchema


class AntennaSchema(SQLAlchemyAutoSchema):
    code_name = fields.String(dump_only=True)

    class Meta:
        model = Antenna
        include_fk = True
        unknown = EXCLUDE


class AntennaPaginatedSchema(PaginatedSchema):
    items = fields.Nested(AntennaSchema, many=True, dump_only=True)
