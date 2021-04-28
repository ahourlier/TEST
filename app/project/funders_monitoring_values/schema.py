from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields, Schema

from app.common.schemas import PaginatedSchema
from app.mission.monitors.schema import MonitorFieldLightSchema
from app.project.funders_monitoring_values import FunderMonitoringValue


class FunderMonitoringValueSchema(SQLAlchemyAutoSchema):
    monitor_field = fields.Nested(MonitorFieldLightSchema)
    value = fields.Raw(allow_none=True)

    class Meta:
        model = FunderMonitoringValue
        include_fk = True
        unknown = EXCLUDE
        exclude = ["date_value", "boolean_value"]


class FunderMonitoringValueLightSchema(SQLAlchemyAutoSchema):
    monitor_field = fields.Nested(MonitorFieldLightSchema)
    value = fields.Raw(allow_none=True, required=True)

    class Meta:
        model = FunderMonitoringValue
        include_fk = True
        unknown = EXCLUDE
        exclude = [
            "date_value",
            "boolean_value",
            "funder_id",
            "created_at",
            "updated_at",
            "monitor_field_id",
            "project_id",
        ]


class FunderMonitoringValuePaginatedSchema(PaginatedSchema):
    items = fields.Nested(FunderMonitoringValueSchema, many=True, dump_only=True)


class InfosFunderSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class FunderMonitoringValueByFunderSchema(Schema):
    funder = fields.Nested(InfosFunderSchema)
    fields = fields.List(fields.Nested(FunderMonitoringValueLightSchema))
