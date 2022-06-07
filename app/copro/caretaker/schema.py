from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.caretaker.model import CareTaker


class CareTakerSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = CareTaker
        include_fk = True


class CareTakerUpdateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = CareTaker
        include_fk = True


class CareTakerCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = CareTaker
        include_fk = True
