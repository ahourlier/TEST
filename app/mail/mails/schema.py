from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE, validate, Schema

from app.mail.mails import Email


class EmailSchema(SQLAlchemyAutoSchema):
    sender_id = fields.Integer(required=False)
    to = fields.List(
        fields.String(validate=validate.Email(error="Not a valid email address")),
        required=False,
    )
    cc = fields.List(
        fields.String(validate=validate.Email(error="Not a valid email address")),
        required=False,
    )
    bcc = fields.List(
        fields.String(validate=validate.Email(error="Not a valid email address")),
        required=False,
    )

    class Meta:
        model = Email
        include_fk = True
        unknown = EXCLUDE


RECIPIENT_REQUESTER_KIND = "REQUESTER"
RECIPIENT_REFERRER_KIND = "REFERRER"

RECIPIENT_KINDS = [RECIPIENT_REFERRER_KIND, RECIPIENT_REQUESTER_KIND]


class EmailProjectsRecipientsInput(Schema):
    project_ids = fields.List(fields.Integer, required=True)
    kind = fields.String(required=True, validate=validate.OneOf(RECIPIENT_KINDS))


class EmailProjectsRecipientsOutput(Schema):
    recipients = fields.List(fields.String())
