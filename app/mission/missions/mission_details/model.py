from app import db
from app.common.base_model import BaseMixin
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from app.admin.subcontractor import MissionDetailSubcontractor
from .elect import Elect


class MissionDetail(BaseMixin, db.Model):
    __tablename__ = "mission_detail"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    # general
    mission_id = Column(
        Integer(), ForeignKey("mission.id"), unique=True, nullable=False
    )
    operational_plan = Column(String(255))
    job = Column(String(255))
    subjob = Column(String(255))
    previous_running_meeting = Column(db.Date, nullable=True)
    partners = relationship("Partner", backref="mission_details")
    # marche et facturation
    market_number = Column(Integer(), nullable=True)
    os_signing_date = Column(db.Date, nullable=True)
    has_sub_contractor = Column(Boolean(), nullable=True)
    billing_type_tf = Column(String(255), nullable=True)
    billing_type_tc = Column(String(255), nullable=True)
    purchase_order_market = Column(Boolean(), nullable=True)
    subcontractor = relationship(
        "Subcontractor",
        secondary=MissionDetailSubcontractor,
        backref=db.backref("mission_detail", lazy="joined"),
    )
    elects = relationship("Elect", backref="mission_details")
    # smq
    smq_starting_meeting = Column(db.Date, nullable=True)
    smq_engagement_meeting = Column(db.Date, nullable=True)
    smq_previous_meeting = Column(db.Date, nullable=True)