from sqlalchemy import Column, Integer, String, select, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber


class Referent(HasPhones, BaseMixin, db.Model):
    """ Referent model """

    __tablename__ = "referent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    function = Column(String(255), nullable=False)
    mission_id = Column(
        Integer(), ForeignKey("mission.id"), unique=False, nullable=False
    )
    active = Column(Boolean(), nullable=True, default=True)

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
