from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.admin.clients.referents import Referent
from app.common.phone_number.schema import PhoneNumberSchema


class ReferentSchema(SQLAlchemyAutoSchema):
    """
    Used for read operations
    """

    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True, skip_none=True)

    class Meta:
        model = Referent
        unknown = EXCLUDE
        include_fk = True
        exclude = (
            "phones",
            "active",
        )


class ReferentCreateMissionSchema(SQLAlchemyAutoSchema):
    """
    Used when creating a mission (mission id does not exist yet)
    Why 2 different schemas instead of setting mission_id to "not required"?
    That way, we have 2 exact representations and not one bulky representation of
    the object we need
    """

    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    class Meta:
        model = Referent
        unknown = EXCLUDE
        exclude = (
            "phones",
            "mission_id",
            "id",
            "active",
        )
