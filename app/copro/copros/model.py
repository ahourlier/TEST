from sqlalchemy import Boolean, String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class Copro:

    __tablename__ = "copro"
    id = Column(Integer(), primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, nullable=True, default=False)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="copros")

