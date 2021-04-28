from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE

from app.perrenoud.thermal_bridges.model import ThermalBridge


class ThermalBridgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ThermalBridge
        include_fk = True
        unknown = EXCLUDE
