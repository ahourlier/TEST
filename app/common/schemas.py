from flask_marshmallow import Schema
from marshmallow import fields


class PaginatedSchema(Schema):
    page = fields.Integer(data_key="page", dump_only=True)
    per_page = fields.Integer(data_key="pageSize", dump_only=True)
    total = fields.Integer(data_key="totalItems", dump_only=True)


class DocumentSchema(Schema):
    files_id = fields.List(fields.String(), required=True)
    kind = fields.String(required=True)
