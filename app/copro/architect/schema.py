from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.address.schema import AddressSchema
from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.architect.model import Architect


class ArchitectSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Architect
        include_fk = True


class ArchitectUpdateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Architect
        include_fk = True


class ArchitectCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Architect
        include_fk = True
