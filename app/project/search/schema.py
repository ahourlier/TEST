from flask_marshmallow.sqla import SQLAlchemyAutoSchema, SQLAlchemySchema
from marshmallow import fields

from app.common.schemas import PaginatedSchema
from app.project.search.model import Search


class FilterSchema(SQLAlchemySchema):
    field = fields.String(required=True)
    op = fields.String(required=True)
    values = fields.List(fields.Raw(allow_none=True), required=True)


class SearchSchema(SQLAlchemySchema):
    term = fields.String()
    filters = fields.List(fields.Nested(FilterSchema()))


class SearchRegisterSchema(SQLAlchemyAutoSchema):
    search = fields.Nested(SearchSchema())

    class Meta:
        model = Search


class SearchDumpSchema(SQLAlchemyAutoSchema):
    request = fields.Nested(SearchSchema())

    class Meta:
        model = Search
        include_fk = True
        exclude = [
            "search",
        ]


class SearchPaginatedSchema(PaginatedSchema):
    items = fields.Nested(SearchDumpSchema, many=True, dump_only=True)
