from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin


class WorkType(BaseMixin, db.Model):
    """WorkType"""

    __tablename__ = "work_type"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    type_name = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship("Project", backref="work_types")
