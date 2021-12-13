from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class LegendeSchema(SQLAlchemyAutoSchema):
    css_class = fields.String()
    text = fields.String()
    icon = fields.String()


class StepMetadataSchema(SQLAlchemyAutoSchema):
    id = fields.String(allow_none=False, required=False)
    name = fields.String()
    order = fields.Integer()
    status = fields.String()
    legendes = fields.Nested(LegendeSchema, many=True)


class StepSchema(SQLAlchemyAutoSchema):
    metadata = fields.Nested(StepMetadataSchema())
    fields = fields.Dict()


class ThematiqueSchema(SQLAlchemyAutoSchema):
    resource_id = fields.Integer()
    id = fields.String(allow_none=False, required=False)
    scope = fields.String()
    thematique_name = fields.String()
    steps = fields.Nested(StepSchema, many=True)


class VersionSchema(ThematiqueSchema):
    version_name = fields.String()
    version_date = fields.String()
