from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.building.model import Building
from app.common.address.schema import AddressSchema
from app.common.schemas import PaginatedSchema


class BuildingCreateSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)
    copro_id = fields.Integer(allow_none=False, required=True)
    name = fields.String(allow_none=False, required=True)

    class Meta:
        model = Building
        include_fk = True


class BuildingSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Building
        include_fk = True


class BuildingPaginatedSchema(PaginatedSchema):
    items = fields.Nested(BuildingSchema(), many=True, dump_only=True)

