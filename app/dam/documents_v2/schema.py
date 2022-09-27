from marshmallow import fields, Schema, validates_schema, EXCLUDE, ValidationError


class HTMLContentSchema(Schema):
    content = fields.Raw(dump_only=True)


class DocumentGenerateSchema(Schema):

    template_id = fields.Integer(required=True)
    source = fields.String(required=True)
    user_email = fields.String(required=True)
    mission_id = fields.Integer(required=True)
    copro_folder_id = fields.Integer(required=False)
    thematic_folder_id = fields.Integer(required=False)

    @validates_schema
    def validate_requires(self, data):
        if data["source"] == "MARKET" and "mission_id" not in data:
            raise ValidationError("mission_id is required when source is 'MARKET")
        if data["source"] == "COPRO" and "copro_folder_id" not in data:
            raise ValidationError("copro_folder_id is required when source is 'COPRO")
        if data["source"] == "THEMATIC" and "thematic_folder_id" not in data:
            raise ValidationError(
                "thematic_folder_id is required when source is 'THEMATIC"
            )

    class Meta:
        unknown = EXCLUDE
