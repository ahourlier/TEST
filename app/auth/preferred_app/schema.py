from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from .model import PreferredApp


class PreferredAppSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PreferredApp
