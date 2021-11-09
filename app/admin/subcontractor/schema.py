from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.common.address.schema import AddressSchema
from app.admin.subcontractor import Subcontractor
from app.common.schemas import PaginatedSchema


class SubcontractorSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema())

    class Meta:
        model = Subcontractor
        include_fk = True
        unknown = EXCLUDE


class SubcontractorPaginatedSchema(PaginatedSchema):
    items = fields.Nested(SubcontractorSchema, many=True, dump_only=True)
