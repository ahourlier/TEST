from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Copro
from ..cadastre.schema import CadastreSchema
from ...auth.users import UserSchema
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    user_in_charge = fields.Nested(UserSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproUpdateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    mission_id = fields.Integer(allow_none=True, required=False)

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


# class CoproLightSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Copro
#         include_fk = False
#         unknown = EXCLUDE


class CoproCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
