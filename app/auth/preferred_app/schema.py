from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

from .model import PreferredApp
from ..users import UserSchema


class PreferredAppSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema, dump_only=True)

    class Meta:
        model = PreferredApp
