from marshmallow import fields, EXCLUDE
from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from app.common.constants import DATE_YEAR_FORMAT
from app.common.phone_number.schema import PhoneNumberSchema
from app.common.schemas import PaginatedSchema
from app.project.contacts import ContactSchema
from app.project.projects import Project
from app.project.requesters.model import Requester
from app.project.taxable_incomes import TaxableIncomeSchema


class RequesterProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True
        unknown = EXCLUDE
        additional = ["code_name"]


class RequesterSchema(SQLAlchemyAutoSchema):
    contacts = fields.List(fields.Nested(ContactSchema()))
    taxable_incomes = fields.List(fields.Nested(TaxableIncomeSchema()))
    phone_number_1 = fields.Nested(PhoneNumberSchema, allow_none=True)
    phone_number_2 = fields.Nested(PhoneNumberSchema, allow_none=True)
    project_type = fields.String(dump_only=True)

    class Meta:
        model = Requester
        include_fk = True
        exclude = ("phones",)
        unknown = EXCLUDE


class RequesterWithProjectSchema(RequesterSchema):
    project = fields.Nested(RequesterProjectSchema, dump_only=True)


class RequesterPaginatedSchema(PaginatedSchema):
    items = fields.Nested(RequesterWithProjectSchema, many=True, dump_only=True)
