from app import db
from app.common.base_model import BaseMixin
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Partner(BaseMixin, db.Model):

    __tablename__ = "partner"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_details_id = Column(
        Integer(), ForeignKey("mission_detail.id"), nullable=False
    )
    name = Column(String(255), nullable=True)
    job = Column(String(255), nullable=True)
    address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", cascade="all, delete", backref="partner", passive_deletes=True)
