from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE
from app.perrenoud.hot_waters.model import HotWater


class HotWaterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HotWater
        include_fk = True
        unknown = EXCLUDE
