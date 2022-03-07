from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin


class Agency(BaseMixin, db.Model):
    """Agency"""

    __tablename__ = "agency"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    postal_address = Column(String(255), nullable=True)
    email_address = Column(String(255), nullable=False)

    @hybrid_property
    def code_name(self):
        return f"{self.id}"
