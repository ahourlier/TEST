from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.common.phone_number.schema import PhoneNumberSchema
from app.mission.missions.mission_details.elect import Elect


class ElectSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Elect
        include_fk = True
        unknown = EXCLUDE
        exclude = (
            "phones",
            "active",
        )


class ElectUpdateSchema(SQLAlchemyAutoSchema):
    mission_details_id = fields.Integer(dump_only=True)
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Elect
        include_fk = True
        unknown = EXCLUDE
        exclude = (
            "phones",
            "active",
        )
