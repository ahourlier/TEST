from sqlalchemy import Boolean, Date, String, Column, Integer, ForeignKey, Text, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class President(HasPhones, BaseMixin, db.Model):
    __tablename__ = "president"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    email_address = Column(String(255))
    election_date = Column(Date, nullable=True)

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
