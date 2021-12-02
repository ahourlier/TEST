from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.building.model import Building
from app.building.settings import NB_LOOP_ACCESS_CODE
from app.common.address.schema import AddressSchema
from app.common.schemas import PaginatedSchema
import base64


class BuildingCreateSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)
    copro_id = fields.Integer(allow_none=False, required=True)
    name = fields.String(allow_none=False, required=True)

    class Meta:
        model = Building
        include_fk = True


class BuildingUpdateSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True, required=False)
    copro_id = fields.Integer(allow_none=True, required=False)
    name = fields.String(allow_none=True, required=False)

    class Meta:
        model = Building
        include_fk = True


class BuildingSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)
    access_code = fields.Method("decode_access_code", dump_only=True)

    def decode_access_code(self, obj):
        if not obj.access_code:
            return ""
        access_code = obj.access_code
        for i in range(0, NB_LOOP_ACCESS_CODE):
            access_code = base64.b64decode(access_code)
        return access_code.decode()

    class Meta:
        model = Building
        include_fk = True


class BuildingForLotSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema(), allow_none=True)

    class Meta:
        model = Building
        include_fk = True


class BuildingPaginatedSchema(PaginatedSchema):
    items = fields.Nested(BuildingSchema(), many=True, dump_only=True)

