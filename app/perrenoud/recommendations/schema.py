from marshmallow import Schema, EXCLUDE, fields


class RecommendationEntitySchema(Schema):
    element_id = fields.Integer(required=True)
    name = fields.String(required=False)
    table = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class RecommendationSchema(Schema):
    recommendation = fields.String(required=True)
    element = fields.Nested(RecommendationEntitySchema(), required=True)

    class Meta:
        unknown = EXCLUDE
