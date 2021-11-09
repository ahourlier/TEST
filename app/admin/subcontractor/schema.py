from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.common.address.schema import AddressSchema
from app.admin.subcontractor import Subcontractor


class SubcontractorSchema(SQLAlchemyAutoSchema):
    address = fields.Nested(AddressSchema())

    class Meta:
        model = Subcontractor
        include_fk = True
        unknown = EXCLUDE
