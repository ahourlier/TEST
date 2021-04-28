from marshmallow import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, Schema

from app.mission.monitors import Monitor
from app.mission.monitors.model import MonitorField


class MonitorFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MonitorField
        include_fk = True
        unknown = EXCLUDE


class MonitorFieldLightSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String()
    type = fields.String()
    invisible = fields.Boolean()
    automatic = fields.Boolean()

    class Meta:
        unknown = EXCLUDE


class MonitorSchema(SQLAlchemyAutoSchema):
    fields = fields.List(fields.Nested(MonitorFieldSchema))

    class Meta:
        model = Monitor
        include_fk = True
        unknown = EXCLUDE
