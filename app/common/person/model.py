from sqlalchemy import Column, Integer, Text, String, select, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Person(HasPhones, BaseMixin, db.Model):
    """ Represents a person """

    __tablename__ = "person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    civility = Column(String(10))
    status = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    company_name = Column(String(255))
    email_address = Column(String(255))
    antenna_id = Column(Integer, ForeignKey("antenna.id"), nullable=True)
    antenna = relationship(
        "Antenna", backref=backref("people", cascade="all, delete")
    )

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
