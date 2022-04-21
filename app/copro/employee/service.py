from app import db
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.copro.employee.interface import EmployeeInterface
from app.copro.employee.model import Employee


class EmployeeService:
    @staticmethod
    def create(new_attrs: EmployeeInterface) -> int:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        new_employee = Employee(**new_attrs)
        db.session.add(new_employee)
        db.session.commit()
        return new_employee.id

    @staticmethod
    def update(employee: Employee, changes: EmployeeInterface):

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    employee, [changes.get("phone_number")]
                )
            else:
                if len(employee.phones) > 0:
                    PhoneNumber.query.filter(
                        PhoneNumber.id == employee.phones[0].id
                    ).delete()
                    db.session.commit()
            del changes["phone_number"]

        employee.update(changes)
        db.session.commit()
        return employee
