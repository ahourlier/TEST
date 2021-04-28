from sqlalchemy import Column, Integer, String, select, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Client(HasPhones, BaseMixin, db.Model):
    """ Client model """

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    postal_address = Column(String(256), nullable=True)
    title = Column(String(20), nullable=True)
    last_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    job_function = Column(String(50), nullable=True)
    email_address = Column(String(255), nullable=True)
    comment = Column(String(500), nullable=True)
    active = Column(Boolean(), nullable=True, default=True)

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
