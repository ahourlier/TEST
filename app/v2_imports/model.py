from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin


class Imports(BaseMixin, db.Model):

    __tablename__ = "imports"

    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref=backref("imports", cascade="all, delete"))
    import_sheet_id = Column(String(50), nullable=False)
    log_sheet_id = Column(String(50))
    status = Column(String(50))
    type = Column(String(50))
