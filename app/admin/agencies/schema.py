from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Agency
from ...common.schemas import PaginatedSchema


class AgencySchema(SQLAlchemyAutoSchema):
    code_name = fields.String(dump_only=True)

    class Meta:
        model = Agency
        unknown = EXCLUDE


class AgencyPaginatedSchema(PaginatedSchema):
    items = fields.Nested(AgencySchema, many=True, dump_only=True)
