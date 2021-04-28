from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, EXCLUDE

from app.common.schemas import PaginatedSchema
from app.project.comments import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    author_id = auto_field(required=False)
    is_important = fields.Boolean(required=False)
    author_first_name = fields.String(dump_only=True, required=False)
    author_last_name = fields.String(dump_only=True, required=False)

    class Meta:
        model = Comment
        include_fk = True
        unknown = EXCLUDE


class CommentPaginatedSchema(PaginatedSchema):
    items = fields.Nested(CommentSchema, many=True, dump_only=True)
