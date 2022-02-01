from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app import db


# class ThematiqueEntity(db.Model):
#     """ Link between thematique in firestore and entity in sql """
#
#     __tablename__ = "thematique_entity"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     resource_type = Column(String(255), nullable=False)
#     resource_id = Column(Integer(), nullable=False)
#     document_id = Column(String(255), nullable=False)


class ThematiqueMission(db.Model):
    """Autorized thematiques per mission"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(Integer(), ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="thematiques")
    thematique_name = Column(String(255), nullable=False)
    authorized = Column(Boolean(), nullable=False, default=True)
