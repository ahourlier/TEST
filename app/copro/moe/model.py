from sqlalchemy import Column, Integer, String, select, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Moe(HasPhones, BaseMixin, db.Model):
    __tablename__ = "moe"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    email_address = Column(String(255))
    comment = Column(String(255))
    address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", cascade="all, delete", backref="moe")

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
