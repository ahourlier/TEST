from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.address.schema import AddressSchema
from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.moe.model import Moe


class MoeSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Moe
        include_fk = True


class MoeUpdateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Moe
        include_fk = True


class MoeCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Moe
        include_fk = True
