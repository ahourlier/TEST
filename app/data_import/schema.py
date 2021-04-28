from marshmallow import Schema, fields, EXCLUDE


class DataImportSchema(Schema):
    mission_id = fields.Integer(required=True)
    data_sheet_id = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
