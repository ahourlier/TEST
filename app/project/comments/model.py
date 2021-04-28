from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app import db
from app.common.base_model import BaseMixin


class Comment(BaseMixin, db.Model):
    """ Comment  """

    __tablename__ = "comment"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    content = Column(String(2083), nullable=True)
    html_content = Column(Text, nullable=True)
    is_important = Column(Boolean(), nullable=False, default=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    project = relationship("Project", backref="comments")
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", backref="comments")

    @hybrid_property
    def author_first_name(self):
        return self.author.first_name

    @hybrid_property
    def author_last_name(self):
        return self.author.last_name
