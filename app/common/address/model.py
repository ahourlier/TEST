from sqlalchemy import Column, Integer, Text, String
from app import db
from app.common.base_model import BaseMixin


class Address(BaseMixin, db.Model):
    """Represents an address"""

    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_address = Column(Text(), nullable=False)
    number = Column(String(50), nullable=False)
    street = Column(String(255), nullable=False)
    postal_code = Column(String(50), nullable=False)
    additional_info = Column(String(255), nullable=True)
    city = Column(String(255), nullable=False)
