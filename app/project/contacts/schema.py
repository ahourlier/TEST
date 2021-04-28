from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields

from app.common.phone_number.schema import PhoneNumberSchema
from app.project.contacts.model import Contact


class ContactSchema(SQLAlchemyAutoSchema):
    requester_id = auto_field(required=False)
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Contact
        include_fk = True
        exclude = ("phones",)
