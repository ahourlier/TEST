from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Syndic
from ..cadastre.schema import CadastreSchema
from ...auth.users import UserSchema
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class SyndicSchema(SQLAlchemyAutoSchema):
    manager_address = fields.Nested(AddressSchema())

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


class SyndicUpdateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    mission_id = fields.Integer(allow_none=True, required=False)

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


# class SyndicLightSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Syndic
#         include_fk = False
#         unknown = EXCLUDE


class SyndicCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


class SyndicPaginatedSchema(PaginatedSchema):
    items = fields.Nested(SyndicSchema(), many=True, dump_only=True)
