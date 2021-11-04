from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.common.address.schema import AddressSchema
from app.mission.missions.mission_details.partner.model import Partner


class PartnerSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema())

    class Meta:
        model = Partner
        include_fk = True
        unknown = EXCLUDE


class PartnerUpdateSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)
    mission_details_id = fields.Integer(dump_only=True)

    class Meta:
        model = Partner
        include_fk = True
        unknown = EXCLUDE
