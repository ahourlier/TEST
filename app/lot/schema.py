from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.schemas import PaginatedSchema
from app.lot import Lot


class LotCreateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=True, allow_none=False)

    class Meta:
        model = Lot
        include_fk = True


class LotUpdateSchema(SQLAlchemyAutoSchema):
    copro_id = fields.Integer(required=False)

    class Meta:
        model = Lot
        include_fk = True


class LotSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Lot
        include_fk = True


class LotPaginatedSchema(PaginatedSchema):
    items = fields.Nested(LotSchema(), many=True, dump_only=True)
