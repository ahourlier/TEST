from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin


class UserTeamPositions:
    MISSION_MANAGER = "mission_manager"
    COLLABORATOR = "collaborator"
    EXTERNAL_COLLABORATOR = "external_collaborator"
    ADDITIONAL_ACCESS = "additional_access"
    CLIENT_ACCESS = "client_access"


class Team(BaseMixin, db.Model):
    """ Team """

    __tablename__ = "team"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_position = Column(
        String(255), nullable=False, default=UserTeamPositions.COLLABORATOR
    )
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=True)
    mission = relationship("Mission", backref="teams")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="teams")
    antenna_id = Column(Integer, ForeignKey("antenna.id"), nullable=True)
    antenna = relationship("Antenna", backref="teams")
    agency_id = Column(Integer, ForeignKey("agency.id"), nullable=True)
    agency = relationship("Agency", backref="teams")
