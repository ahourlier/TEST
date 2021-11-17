from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Copro
from ..cadastre.schema import CadastreSchema
from ..president.schema import PresidentSchema, PresidentCreateSchema
from ..syndic.schema import SyndicSchema, SyndicCreateSchema
from ...auth.users import UserSchema
from ...auth.users.schema import UserLightSchema
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema())
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    syndics = fields.List(fields.Nested(SyndicSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    user_in_charge = fields.Nested(UserLightSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproUpdateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    mission_id = fields.Integer(allow_none=True, required=False)
    president = fields.Nested(PresidentCreateSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    syndics = fields.List(fields.Nested(SyndicCreateSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema())
    president = fields.Nested(PresidentCreateSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
