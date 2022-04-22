from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.fire_safety_personnel.model import FireSafetyPersonnel


class FireSafetyPersonnelSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = FireSafetyPersonnel
        include_fk = True


class FireSafetyPersonnelUpdateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = FireSafetyPersonnel
        include_fk = True


class FireSafetyPersonnelCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = FireSafetyPersonnel
        include_fk = True
