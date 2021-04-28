from marshmallow import Schema, fields, EXCLUDE


class HomepageActionsSchema(Schema):
    count_meet_advices_to_plan = fields.Integer()
    count_meet_to_process = fields.Integer()
    count_contact_to_call_again = fields.Integer()
    count_call_after_meet_advice = fields.Integer()
    count_payment_request = fields.Integer()
    count_ANAH = fields.Integer()

    class Meta:
        unkwnown: EXCLUDE
