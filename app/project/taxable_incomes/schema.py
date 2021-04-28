from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields

from app.common.constants import DATE_YEAR_FORMAT
from app.project.taxable_incomes.model import TaxableIncome


class TaxableIncomeSchema(SQLAlchemyAutoSchema):
    requester_id = auto_field(required=False)

    class Meta:
        model = TaxableIncome
        include_fk = True
