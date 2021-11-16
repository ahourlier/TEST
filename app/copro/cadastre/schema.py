from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE
from .model import Cadastre


class CadastreSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Cadastre
        unknown = EXCLUDE
