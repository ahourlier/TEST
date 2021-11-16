from sqlalchemy import Boolean, String, Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from app import db

# from app.common.address.model import Address
from app.common.base_model import BaseMixin


class Syndic(BaseMixin, db.Model):
    __tablename__ = "syndic"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    copro_id = Column(Integer, ForeignKey("copro.id"), nullable=False)
    copro = relationship("Copro", backref="syndics")
    name = Column(String(255))
    type = Column(String(255))
    manager_name = Column(String(255))
    manager_address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    manager_address = relationship(
        "Address", cascade="all, delete", passive_deletes=True,
    )
    manager_email = Column(String(255))
    comment = Column(Text())
