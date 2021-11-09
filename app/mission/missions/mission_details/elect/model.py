from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Float, select
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin
from app.common.phone_number.model import HasPhones, PhoneNumber
from sqlalchemy.ext.hybrid import hybrid_property


class Elect(BaseMixin, db.Model):

    __tablename__ = "elect"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_details_id = Column(
        Integer(), ForeignKey("mission_detail.id"), nullable=False
    )
    last_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    function = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

    @hybrid_property
    def phone_number(self):
        return self.phones[0] if self.phones else None

    @phone_number.expression
    def phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
