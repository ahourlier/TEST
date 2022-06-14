from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.mission.missions.mission_details.financial_device import FinancialDevice


class FinancialDeviceSchema(SQLAlchemyAutoSchema):
    mission_details_id = fields.Integer(required=True)

    class Meta:
        model = FinancialDevice
        include_fk = True
        unknown = EXCLUDE


class FinancialDevicesSchema(FinancialDeviceSchema):
    financial_devices = fields.List(fields.Nested(FinancialDeviceSchema))


class FinancialDeviceUpdateSchema(SQLAlchemyAutoSchema):
    mission_details_id = fields.Integer(required=False)

    class Meta:
        model = FinancialDevice
        include_fk = True
        unknown = EXCLUDE
