from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Employee(HasPhones, BaseMixin, db.Model):
    __tablename__ = "employee"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    comment = Column(String(255))

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
