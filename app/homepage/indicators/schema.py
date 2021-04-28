from marshmallow import Schema, EXCLUDE, fields


class IndicatorFilterSchema(Schema):
    missions_id = fields.List(fields.Integer, required=True, allow_none=False)

    class Meta:
        unknown: EXCLUDE


class DatasetSchema(Schema):
    data = fields.List(fields.Integer)

    class Meta:
        unkwnown: EXCLUDE


class IndicatorSchema(Schema):

    labels = fields.List(fields.String)
    datasets = fields.List(fields.Nested(DatasetSchema))

    class Meta:
        unkwnown: EXCLUDE
