from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.auth.users.schema import UserSchema

from app.common.schemas import PaginatedSchema
from app.thematique.historics.model import Historic


class HistoricSchema(SQLAlchemyAutoSchema):
    updated_by = fields.Nested(UserSchema(), dump_only=True)

    class Meta:
        model = Historic
        include_fk = True
        unknown = EXCLUDE
        exclude = ('updated_by_id',)  # Already present in updated_by


class HistoricPaginatedSchema(PaginatedSchema):
    items = fields.Nested(HistoricSchema, many=True, dump_only=True)
