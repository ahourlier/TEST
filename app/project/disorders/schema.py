from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import INCLUDE, fields

from app.project.disorders.model import Disorder, DisorderType


class DisorderTypeSchema(SQLAlchemyAutoSchema):
    disorder_id = fields.Integer(required=False)

    class Meta:
        model = DisorderType
        include_fk = True
        unknown = INCLUDE


class DisorderSchema(SQLAlchemyAutoSchema):
    accommodation_id = fields.Integer(required=False, allow_none=True)
    common_area_id = fields.Integer(required=False, allow_none=True)
    disorder_types = fields.List(fields.Nested(DisorderTypeSchema, allow_none=False))

    class Meta:
        model = Disorder
        include_fk = True
        unknown = INCLUDE
