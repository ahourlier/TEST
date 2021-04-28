from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, EXCLUDE

from app.common.phone_number.schema import PhoneNumberSchema
from app.common.schemas import PaginatedSchema
from app.project.accommodations import Accommodation
from app.project.disorders import DisorderSchema


class AccommodationSchema(SQLAlchemyAutoSchema):
    disorders = fields.List(fields.Nested(DisorderSchema()))
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)
    initial_state_id = fields.Integer(required=False, allow_none=True, dump_only=True)

    class Meta:
        model = Accommodation
        include_fk = True
        exclude = ("phones",)
        unknown = EXCLUDE


class AccommodationLightSchema(Schema):
    id = fields.Integer()
    name = fields.String(allow_none=True)
    living_area = fields.Float(allow_none=True)
    additional_area = fields.Float(allow_none=True)

    class Meta:
        model = Accommodation
        unknown = EXCLUDE


class AccommodationPaginatedSchema(PaginatedSchema):
    items = fields.Nested(AccommodationSchema, many=True, dump_only=True)
