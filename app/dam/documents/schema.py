from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, EXCLUDE

from .model import Document
from ...common.schemas import PaginatedSchema


class HTMLContentSchema(Schema):
    content = fields.Raw(dump_only=True)


class DocumentRequestSchema(Schema):
    project_id = fields.Integer(required=True)
    template_id = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class DocumentGenerateSchema(Schema):
    project_id = fields.Integer(required=True)
    template_id = fields.String(required=True)
    source = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class DocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        include_fk = True


class DocumentPaginatedSchema(PaginatedSchema):
    items = fields.Nested(DocumentSchema, many=True, dump_only=True)
