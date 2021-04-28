from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import EXCLUDE, fields

from app.common.constants import DATE_YEAR_FORMAT
from app.project.common_areas import CommonArea
from app.project.disorders import DisorderSchema


class CommonAreaSchema(SQLAlchemyAutoSchema):
    disorders = fields.List(fields.Nested(DisorderSchema()))
    project_id = fields.Integer(required=False)

    class Meta:
        model = CommonArea
        include_fk = True
        unknown = EXCLUDE
