from app import db, metadata
from app.common.base_model import BaseMixin
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

MissionDetailSubcontractor = Table(
    "mission_detail_subcontractor",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("subcontractor_id", Integer, ForeignKey("subcontractor.id")),
    Column("mission_detail_id", Integer, ForeignKey("mission_detail.id")),
)


class Subcontractor(BaseMixin, db.Model):
    __tablename__ = "subcontractor"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    job = Column(String(255))
    address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", cascade="all, delete", backref="subcontractor")
    mission_details = relationship(
        "MissionDetail",
        secondary=MissionDetailSubcontractor,
        backref=db.backref("subcontractors", lazy="joined"),
    )
    active = Column(Boolean(), nullable=True, default=True)
