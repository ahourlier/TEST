from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.common.schemas import PaginatedSchema
from app.mission.custom_fields import CustomField
from app.mission.custom_fields.model import AvailableFieldValue


class AvailableFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE
        model = AvailableFieldValue
        exclude = ["is_deleted", "created_at", "updated_at"]


class CustomFieldSchema(SQLAlchemyAutoSchema):
    available_values = fields.List(
        fields.Nested(AvailableFieldSchema()), required=False, allow_none=True
    )

    class Meta:
        unknown = EXCLUDE
        model = CustomField
        include_fk = True


class CustomFieldPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CustomFieldSchema, many=True, dump_only=True)
