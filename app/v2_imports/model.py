from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db
import enum
from app.common.base_model import BaseMixin


class ImportType(enum.Enum):
    SCAN = "SCAN"
    IMPORT = "IMPORT"


class ImportStatus(enum.Enum):
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    DONE = "DONE"


class Imports(BaseMixin, db.Model):

    __tablename__ = "imports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref=backref("imports", cascade="all, delete"))
    import_sheet_id = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    log_sheet_id = Column(String(50))
    status = Column(String(50))
    type = Column(String(50))
