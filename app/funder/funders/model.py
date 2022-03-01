from sqlalchemy import Column, Integer, String, ForeignKey, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin

# needs to be imported in order to define the relationship
from app.mission.missions.model import Mission


class Funder(SoftDeletableMixin, BaseMixin, db.Model):
    """ Represents a funder """

    __tablename__ = "funder"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subvention_round = Column(Integer, nullable=False, default=2)  # number of decimals
    type = Column(String(255), nullable=False)
    priority = Column(Integer, nullable=True, default=1000)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=True)
    mission = relationship("Mission", backref="funders")
    requester_type = Column(String(255), nullable=True)
    position = Column(Integer, nullable=True)

    @hybrid_property
    def is_national(self):
        return self.mission_id is None

    @is_national.expression
    def is_national(cls):
        return cls.mission_id == None

    @hybrid_property
    def is_duplicate(self):
        return len(self.simulation_duplicate_funders) != 0

    @hybrid_property
    def is_linked_to_simulation(self):
        return (
            len(self.simulation_base_funders) != 0
            or len(self.deposit_simulations) != 0
            or len(self.payment_request_simulations) != 0
            or len(self.certified_simulations) != 0
        )

    @is_duplicate.expression
    def is_duplicate(cls):
        from app.project.simulations.model import SimulationFunder

        return (
            select([func.count(SimulationFunder.id)]).where(
                SimulationFunder.duplicate_funder_id == cls.id
            )
        ).as_scalar() != 0
