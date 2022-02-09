from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
import json
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin

FORBIDDEN_FIELDS = [
    "_sa_instance_state",
    "status",
    "required_action",
    "address_location",
    "type",
    "work_type",
    "closed",
    "closure_motive",
    "urgent_visit",
    "secondary_case_type",
]


class Search(BaseMixin, db.Model):
    """ Search  """

    __tablename__ = "search"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    is_favorite = Column(Boolean(), nullable=False, default=False)
    search = Column(Text(), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="searchs")

    @hybrid_property
    def request(self):
        return json.loads(self.search)
