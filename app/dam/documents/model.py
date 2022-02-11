from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin


class Document(BaseMixin, db.Model):
    """Document"""

    __tablename__ = "document"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    template_id = Column(String(255), nullable=True)
    document_id = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship("Project", backref="documents")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="documents")
    status = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)
