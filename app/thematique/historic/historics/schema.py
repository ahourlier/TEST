from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.schemas import PaginatedSchema
from app.thematique.historic.historics.model import Historic


class HistoricSchema(SQLAlchemyAutoSchema):
    pass

    class Meta:
        model = Historic
        include_fk = True
        unknown = EXCLUDE


class HistoricPaginatedSchema(PaginatedSchema):
    items = fields.Nested(HistoricSchema, many=True, dump_only=True)
