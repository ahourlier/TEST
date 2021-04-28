from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE
from app.perrenoud.areas import Area


class AreaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Area
        include_fk = True
        unknown = EXCLUDE
