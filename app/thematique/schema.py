from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Legende(SQLAlchemyAutoSchema):
    css_class = fields.String()
    text = fields.String()
    icon = fields.String()


class StepMetadata(SQLAlchemyAutoSchema):
    id = fields.String(allow_none=False, required=False)
    name = fields.String()
    order = fields.Integer()
    status = fields.String()
    legendes = fields.Nested(Legende, many=True)


class Step(SQLAlchemyAutoSchema):
    metadata = fields.Nested(StepMetadata())
    fields = fields.Dict()


class Thematique(SQLAlchemyAutoSchema):
    resource_id = fields.Integer()
    id = fields.String(allow_none=False, required=False)
    scope = fields.String()
    thematique_name = fields.String()
    steps = fields.Nested(Step, many=True)


class Version(Thematique):
    version_name = fields.String()
    version_date = fields.String()
