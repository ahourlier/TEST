from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class ProjectLead(BaseMixin, db.Model):
    """ Supervisor """

    __tablename__ = "project_lead"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship(
        "Project", backref=backref("project_leads", cascade="all,delete")
    )
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="project_leads")
