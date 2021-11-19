from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Syndic
from ...common.address.schema import AddressSchema
from ...common.schemas import PaginatedSchema


class SyndicSchema(SQLAlchemyAutoSchema):
    manager_address = fields.Nested(AddressSchema(), allow_none=None, required=False)

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


class SyndicUpdateSchema(SQLAlchemyAutoSchema):
    manager_address = fields.Nested(AddressSchema(), allow_none=None, required=False)
    copro_id = fields.Integer(allow_none=None, required=False)

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


# class SyndicLightSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Syndic
#         include_fk = False
#         unknown = EXCLUDE


class SyndicCreateSchema(SQLAlchemyAutoSchema):
    manager_address = fields.Nested(AddressSchema(), allow_none=None, required=False)
    copro_id = fields.Integer(allow_none=None, required=False)

    class Meta:
        model = Syndic
        include_fk = True
        unknown = EXCLUDE


class SyndicPaginatedSchema(PaginatedSchema):
    items = fields.Nested(SyndicSchema(), many=True, dump_only=True)
