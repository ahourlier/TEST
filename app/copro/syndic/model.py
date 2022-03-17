from sqlalchemy import Boolean, String, Column, Integer, ForeignKey, Text, select, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db

# from app.common.address.model import Address
from app.common.base_model import BaseMixin
from app.common.phone_number.model import PhoneNumber, HasPhones


class Syndic(HasPhones, BaseMixin, db.Model):
    __tablename__ = "syndic"

    id = Column(Integer(), primary_key=True, autoincrement=True)

    cs_id = Column(Integer, ForeignKey("combined_structure.id"), nullable=True)
    cs = relationship("CombinedStructure", backref="syndics")
    name = Column(String(255))
    type = Column(String(255))
    contract_date = Column(Date)
    manager_name = Column(String(255))
    manager_address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    manager_address = relationship(
        "Address",
        cascade="all, delete",
    )
    manager_email = Column(String(255))
    comment = Column(Text())

    @hybrid_property
    def manager_phone_number(self):
        return self.phones[0] if self.phones else None

    @manager_phone_number.expression
    def manager_phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()
