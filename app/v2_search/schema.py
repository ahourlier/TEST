from marshmallow import fields, INCLUDE
from flask_marshmallow import Schema


class SearchStructureSchema(Schema):
    name = fields.String(dump_only=True, required=True)
    label = fields.String(dump_only=True, required=True)
    type = fields.String(dump_only=True, required=True)
    is_default = fields.String(dump_only=True, required=True)
    values = fields.List(fields.String(dump_only=True), required=False)


class SearchItemsStructureSchema(Schema):
    entity: fields.String(dump_only=True, required=True)
    items: fields.List(fields.Nested(SearchStructureSchema()), dump_only=True)

    class Meta:
        fields = ("entity", "items")
