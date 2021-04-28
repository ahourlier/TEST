from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, EXCLUDE

from app.common.schemas import PaginatedSchema
from app.project.project_custom_fields import CustomFieldValue
from app.project.project_custom_fields.model import ProjectCustomField


class CustomFieldValueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CustomFieldValue
        exclude = ["created_at", "updated_at", "is_deleted"]
        unknown = EXCLUDE


class ProjectCustomFieldSchema(SQLAlchemyAutoSchema):
    multiple_values = fields.List(
        fields.Nested(CustomFieldValueSchema), allow_none=True
    )

    class Meta:
        model = ProjectCustomField
        include_fk = True
        exclude = ["created_at", "updated_at", "is_deleted"]
        unknown = EXCLUDE


class ProjectCustomFieldPaginatedSchema(PaginatedSchema):
    items = fields.Nested(ProjectCustomFieldSchema, many=True, dump_only=True)
