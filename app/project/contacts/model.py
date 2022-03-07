from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import PhoneNumber, HasPhones


class Contact(HasPhones, BaseMixin, db.Model):
    """Contact"""

    __tablename__ = "contact"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    main_contact = Column(Boolean(create_constraint=False), nullable=True)
    email = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    title = Column(String(10), nullable=True)
    comment = Column(String(255), nullable=True)
    requester_id = Column(Integer, ForeignKey("requester.id"), nullable=False)
    requester = relationship(
        "Requester", backref=backref("contacts", cascade="all,delete")
    )

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
