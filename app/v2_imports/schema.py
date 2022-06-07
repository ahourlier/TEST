from pickle import FALSE
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE
from app.auth.users.schema import UserLightSchema
from app.common.schemas import PaginatedSchema

from app.v2_imports.model import Imports


class ImportsSchema(SQLAlchemyAutoSchema):
    log_sheet_id = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    type = fields.String(dump_only=True)
    mission_id = fields.Integer(dump_only=True)
    author_id = fields.Integer(dump_only=True)
    author = fields.Nested(UserLightSchema(), dump_only=True)

    class Meta:
        model = Imports


class ImportsPaginatedSchema(PaginatedSchema):
    items = fields.Nested(ImportsSchema, many=True, dump_only=True)
