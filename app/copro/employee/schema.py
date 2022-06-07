from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.common.phone_number.schema import PhoneNumberSchema
from app.copro.employee.model import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = Employee
        include_fk = True


class EmployeeUpdateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = Employee
        include_fk = True


class EmployeeCreateSchema(SQLAlchemyAutoSchema):
    phone_number = fields.Nested(PhoneNumberSchema(), allow_none=True)

    class Meta:
        model = Employee
        include_fk = True
