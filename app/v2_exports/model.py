from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db
import enum
from app.common.base_model import BaseMixin


class ExportStatus(enum.Enum):
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    DONE = "DONE"


class Exports(BaseMixin, db.Model):

    __tablename__ = "exports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref=backref("exports", cascade="all, delete"))
    export_sheet_id = Column(String(50), nullable=True)
    name = Column(String(255), nullable=False)
    export_type = Column(String(255), nullable=True)
    status = Column(String(50))
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", backref="exports")
