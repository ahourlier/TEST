from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.admin.clients.referents import Referent
from app.common.phone_number.schema import PhoneNumberSchema


class ReferentSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Referent
        unknown = EXCLUDE
        include_fk = True
        exclude = (
            "phones",
            "active",
        )
