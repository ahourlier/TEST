from marshmallow import EXCLUDE, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.president.model import President


class PresidentSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), dump_only=True)

    class Meta:
        model = President


class PresidentCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)
    copro_id = fields.Integer(allow_none=True, required=False)
    cs_id = fields.Integer(allow_none=True, required=False)

    class Meta:
        model = President
        include_fk = True
        unknown = EXCLUDE
