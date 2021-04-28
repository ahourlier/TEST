from marshmallow import EXCLUDE, Schema, fields


class PhotoSchema(Schema):
    name = fields.String(required=True)
    drive_id = fields.String(required=True)
    url = fields.String(required=False)

    class Meta:
        include_fk = True
        unknown = EXCLUDE


class PhotoIdentitySchema(Schema):
    id = fields.String(required=True)
    filename = fields.String(required=True)


class PhotoAddSchema(Schema):
    photos = fields.List(fields.Nested(PhotoIdentitySchema()), required=True)
    section = fields.String(required=True)
    accommodation_id = fields.Integer(required=False, allow_none=True)
    room_id = fields.Integer(required=False, allow_none=True)
    scenario_id = fields.Integer(required=False, allow_none=True)


class PhotoFetchSchema(Schema):
    project_id = fields.Integer(required=True)
    section = fields.String(required=False)
    accommodation_id = fields.Integer(required=False)
    room_id = fields.Integer(required=False)
    scenario_id = fields.Integer(required=False)
