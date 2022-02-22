from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from app.auth.users.schema import UserLightSchema
from app.common.schemas import PaginatedSchema
from app.task.model import Task


class TaskSchema(SQLAlchemyAutoSchema):
    assignee = fields.Nested(UserLightSchema(), dump_only=True)
    author = fields.Nested(UserLightSchema(), dump_only=True)
    mission_id = fields.Integer(allow_none=False, required=True)
    author_id = fields.Integer(dump_only=True)
    assignee_id = fields.Integer(allow_none=True, required=False)
    status = fields.String(allow_none=False, required=True)
    step_id = fields.String(allow_none=False, required=True)
    version_id = fields.String(allow_none=False, required=True)
    task_type = fields.String(allow_none=True, required=False)

    class Meta:
        model = Task


class TaskPaginatedSchema(PaginatedSchema):
    items = fields.Nested(TaskSchema, many=True, dump_only=True)


class TaskUpdateSchema(SQLAlchemyAutoSchema):
    mission_id = fields.Integer(allow_none=False, required=False)
    assignee_id = fields.Integer(allow_none=True, required=False)
    task_type = fields.String(allow_none=True, required=False)

    class Meta:
        model = Task
        unknown = EXCLUDE
