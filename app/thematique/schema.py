from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.thematique import ThematiqueMission


class LegendeSchema(SQLAlchemyAutoSchema):
    css_class = fields.String()
    text = fields.String()
    icon = fields.String()


class StepMetadataSchema(SQLAlchemyAutoSchema):
    id = fields.String(allow_none=False, required=False)
    label = fields.String()
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
    label = fields.String()
    thematique_name = fields.String()
    steps = fields.Nested(StepSchema, many=True)


class VersionSchema(ThematiqueSchema):
    version_name = fields.String(allow_none=False, required=True)
    version_date = fields.String(allow_none=False, required=True)


class ThematiqueMissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ThematiqueMission
        include_fk = True
        unknown = EXCLUDE
