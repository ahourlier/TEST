from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Copro
from ..cadastre.schema import CadastreSchema
from ..moe.schema import MoeSchema, MoeUpdateSchema, MoeCreateSchema
from ..president.schema import PresidentSchema, PresidentCreateSchema
from ..syndic.schema import SyndicSchema, SyndicCreateSchema
from ...auth.users.schema import UserInChargeSchema
from ...common.phone_number.schema import PhoneNumberSchema
from ...cle_repartition.schema import CleRepartitionSchema, CleRepartitionCreateSchema
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):
    president = fields.Nested(PresidentSchema(), dump_only=True)
    cadastres = fields.List(fields.Nested(CadastreSchema()), dump_only=True)
    syndics = fields.List(fields.Nested(SyndicSchema()), dump_only=True)
    address_1 = fields.Nested(AddressSchema(), dump_only=True)
    address_2 = fields.Nested(AddressSchema(), dump_only=True)
    syndic_manager_address = fields.Nested(AddressSchema(), dump_only=True)
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), dump_only=True)
    admin_manager_address = fields.Nested(AddressSchema(), dump_only=True)
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), dump_only=True)
    user_in_charge = fields.Nested(UserInChargeSchema(), dump_only=True)
    moe = fields.Nested(MoeSchema(), dump_only=True)
    cles_repartition = fields.List(fields.Nested(CleRepartitionSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproUpdateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(
        fields.Nested(CadastreSchema()), allow_none=True, required=False
    )
    address_1 = fields.Nested(AddressSchema(), allow_none=True, required=False)
    address_2 = fields.Nested(AddressSchema(), allow_none=True, required=False)
    syndic_manager_address = fields.Nested(
        AddressSchema(), allow_none=None, required=False
    )
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    admin_manager_address = fields.Nested(
        AddressSchema(), allow_none=None, required=False
    )
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    mission_id = fields.Integer(allow_none=True, required=False)
    president = fields.Nested(PresidentCreateSchema(), allow_none=True, required=False)
    moe = fields.Nested(MoeUpdateSchema(), required=False, allow_none=True)
    cles_repartition = fields.List(fields.Nested(CleRepartitionCreateSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))
    syndics = fields.List(fields.Nested(SyndicCreateSchema()))
    address_1 = fields.Nested(AddressSchema())
    address_2 = fields.Nested(AddressSchema(), required=False, allow_none=True)
    syndic_manager_address = fields.Nested(
        AddressSchema(), allow_none=None, required=False
    )
    syndic_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    admin_manager_address = fields.Nested(
        AddressSchema(), allow_none=None, required=False
    )
    admin_manager_phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    president = fields.Nested(PresidentCreateSchema())
    copro_type = fields.String(required=True, allow_none=False)
    moe = fields.Nested(MoeCreateSchema(), required=False, allow_none=True)
    cles_repartition = fields.List(fields.Nested(CleRepartitionCreateSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproForLotsSchema(SQLAlchemyAutoSchema):
    address_1 = fields.Nested(AddressSchema())
    user_in_charge = fields.Nested(UserInChargeSchema(), dump_only=True)

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproLightSchema(SQLAlchemyAutoSchema):
    address_1 = fields.Nested(AddressSchema())

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
