from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin

# for relationship
from app.admin.agencies import Agency


class Antenna(BaseMixin, db.Model):
    """Antenna"""

    __tablename__ = "antenna"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    postal_address = Column(String(255), nullable=True)
    email_address = Column(String(255), nullable=False)
    agency_id = Column(Integer, ForeignKey("agency.id"), nullable=False)
    agency = relationship("Agency", backref="antennas")

    @hybrid_property
    def code_name(self):
        return f"{self.id}"
