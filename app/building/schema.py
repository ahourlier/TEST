from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.building.model import Building
from app.common.address.schema import AddressSchema


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


class BuildingPaginatedSchema(SQLAlchemyAutoSchema):
    items = fields.List(fields.Nested(BuildingSchema()), dump_only=True)
