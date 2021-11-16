from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from .model import Copro
from ..cadastre.schema import CadastreSchema
from ...common.schemas import PaginatedSchema


class CoproSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


# class CoproLightSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Copro
#         include_fk = False
#         unknown = EXCLUDE


class CoproCreateSchema(SQLAlchemyAutoSchema):
    cadastres = fields.List(fields.Nested(CadastreSchema()))

    class Meta:
        model = Copro
        include_fk = True
        unknown = EXCLUDE


class CoproPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CoproSchema(), many=True, dump_only=True)
