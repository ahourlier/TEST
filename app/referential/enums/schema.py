from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, Schema, fields

from app.referential.enums import PerrenoudEnum


class PerrenoudEnumSchema(Schema):
    value = fields.Integer()
    label = fields.String()

    class Meta:
        include_fk = True
        unknown = EXCLUDE


class EnumsFetchSchema(Schema):
    enums = fields.List(fields.Integer())


class CompleteEnumSchema(Schema):
    name = fields.String()
    index = fields.Integer()
    items = fields.List(fields.Nested(PerrenoudEnumSchema()))
