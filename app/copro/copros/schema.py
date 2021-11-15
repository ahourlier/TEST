from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Copro
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


# class CoproLightSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Copro
#         include_fk = False
#         unknown = EXCLUDE


# class CoproCreateSchema(SQLAlchemyAutoSchema):
#     agency = fields.Nested(AgencySchema())
#     antenna = fields.Nested(AntennaSchema())
#     client = fields.Nested(ClientSchema())
#     code_name = fields.String(dump_only=True)
#
#     class Meta:
#         model = Copro
#         include_fk = True
#         unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
