from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field

from app.common.phone_number.model import PhoneNumber


class PhoneNumberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PhoneNumber
        exclude = ("resource_type", "resource_id", "created_at", "updated_at")

    national = auto_field(data_key="formatNational")
    international = auto_field(data_key="formatInternational")
    country_code = auto_field(data_key="countryCode")
