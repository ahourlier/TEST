from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Client
from ...common.phone_number.schema import PhoneNumberSchema
from ...common.schemas import PaginatedSchema


class ClientSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Client
        unknown = EXCLUDE
        exclude = (
            "phones",
            "active",
        )


class ClientPaginatedSchema(PaginatedSchema):
    items = fields.Nested(ClientSchema, many=True, dump_only=True)
