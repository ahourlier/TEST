from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.project.work_types.model import WorkType


class WorkTypeSchema(SQLAlchemyAutoSchema):
    project_id = fields.Integer(required=False)

    class Meta:
        model = WorkType
