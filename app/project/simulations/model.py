from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from app import db
from app.common.base_model import BaseMixin

SIMULATIONS_USE_CASES = ["Dépôt", "Dossier agréé", "Paiement"]
SIMULATIONS_KEYWORD_SORT = {
    "deposit": "Dépôt",
    "certified": "Dossier agréé",
    "payment": "Paiement",
}


class SimulationSubResult(BaseMixin, db.Model):
    """SimulationSubResult table"""

    __tablename__ = "simulation_sub_result"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship(
        "Simulation",
        foreign_keys="SimulationSubResult.simulation_id",
        backref="sub_results",
    )
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship(
        "Accommodation",
        foreign_keys="SimulationSubResult.accommodation_id",
        backref="sub_results",
    )
    work_price = Column(Float(), nullable=True)
    total_subvention = Column(Float(), nullable=True)
    remaining_cost = Column(Float(), nullable=True)
    subvention_on_TTC = Column(Integer(), nullable=True)
    is_common_area = Column(Boolean(), nullable=True, default=False)


class SimulationAccommodation(BaseMixin, db.Model):
    """SimulationAccommodation"""

    __tablename__ = "simulation_accommodation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship(
        "Simulation",
        foreign_keys="SimulationAccommodation.simulation_id",
        backref="simulations_accommodations",
    )
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship("Accommodation", backref="accommodations_simulations")

    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)
    
    rent_type = Column(String(255), nullable=True)
    rent_per_msq = Column(Float(), nullable=True)
    rent = Column(Float(), nullable=True)


class SimulationQuote(BaseMixin, db.Model):
    """SimulationQuote"""

    __tablename__ = "simulation_quote"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    base_quote_id = Column(Integer, ForeignKey("quote.id"), nullable=True)
    base_quote = relationship(
        "Quote",
        foreign_keys="SimulationQuote.base_quote_id",
        backref=backref("simulation_base_quotes", cascade="all, delete"),
    )
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship("Simulation", backref="simulation_quotes")


class SimulationFunder(BaseMixin, db.Model):
    """SimulationFunder"""

    __tablename__ = "simulation_funder"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    base_funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    base_funder = relationship(
        "Funder",
        foreign_keys="SimulationFunder.base_funder_id",
        backref="simulation_base_funders",
    )
    duplicate_funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    duplicate_funder = relationship(
        "Funder",
        foreign_keys="SimulationFunder.duplicate_funder_id",
        backref="simulation_duplicate_funders",
    )
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship(
        "Simulation",
        backref=backref("simulation_funders", order_by="SimulationFunder.created_at"),
    )
    match_scenario_id = Column(
        Integer, ForeignKey("funding_scenario.id"), nullable=True
    )
    match_scenario = relationship("FundingScenario", backref="match_simulation_funders")
    rate = Column(Integer, nullable=True)
    advance = Column(Float, nullable=True)
    subventioned_expense = Column(Float, nullable=True)
    eligible_cost = Column(Float, nullable=True)
    upper_limit = Column(Float, nullable=True)
    subvention = Column(Float, nullable=True)
    work_price = Column(Float, nullable=True)
    remaining_cost = Column(Float, nullable=True)
    subvention_on_TTC = Column(Integer, nullable=True)


class SimulationDeposit(BaseMixin, db.Model):
    """SimulationDeposit"""

    __tablename__ = "simulation_deposit"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    deposit_date = db.Column(db.Date, nullable=True)
    funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    funder = relationship(
        "Funder",
        foreign_keys="SimulationDeposit.funder_id",
        backref="deposit_simulations",
    )
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship("Simulation", backref="deposit_funders")


class SimulationPaymentRequest(BaseMixin, db.Model):
    """SimulationPaymentRequest"""

    __tablename__ = "simulation_payment_request"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    payment_request_date = db.Column(db.Date, nullable=True)
    funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    funder = relationship(
        "Funder",
        foreign_keys="SimulationPaymentRequest.funder_id",
        backref="payment_request_simulations",
    )
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship("Simulation", backref="payment_request_funders")


class SimulationCertified(BaseMixin, db.Model):
    """SimulationCertified"""

    __tablename__ = "simulation_certified"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    certification_date = db.Column(db.Date, nullable=True)
    funder_id = Column(Integer, ForeignKey("funder.id"), nullable=True)
    funder = relationship(
        "Funder",
        foreign_keys="SimulationCertified.funder_id",
        backref="certified_simulations",
    )
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship("Simulation", backref="certification_funders")


class FunderAccommodation(BaseMixin, db.Model):
    """FunderAccommodation"""

    __tablename__ = "funder_accommodations"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    simulation_funder_id = Column(
        Integer, ForeignKey("simulation_funder.id"), nullable=True
    )
    simulation_funder = relationship(
        "SimulationFunder",
        foreign_keys="FunderAccommodation.simulation_funder_id",
        backref=backref(
            "funder_accommodations", order_by="asc(FunderAccommodation.id)"
        ),
    )
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship("Accommodation", backref="accommodation_funders")
    scenario_id = Column(Integer, ForeignKey("funding_scenario.id"), nullable=True)
    scenario = relationship(
        "FundingScenario", backref="scenarios_funders_accommodations"
    )
    rate = Column(Integer, nullable=True)
    is_common_area = Column(Boolean, nullable=True, default=False)
    subventioned_expense = Column(Float, nullable=True)
    eligible_cost = Column(Float, nullable=True)
    upper_limit = Column(Float, nullable=True)
    subvention = Column(Float, nullable=True)

    @hybrid_property
    def common_area_surface(self):
        # In case this FunderAccommodation is a common area, the front may need
        # the common area surface. We retrieve it as an hybrid property
        if not self.is_common_area:
            return None
        project_common_area = self.simulation_funder.simulation.project.common_areas
        return (
            0
            if project_common_area is None or project_common_area.area is None
            else project_common_area.area
        )


class Simulation(BaseMixin, db.Model):
    """Simulation"""

    __tablename__ = "simulation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    project = relationship("Project", backref="simulations")
    quotes_modified = Column(Boolean(), default=False)
    note_certifications = Column(String(2083), nullable=True)
    note_payment_requests = Column(String(2083), nullable=True)
    note_deposits = Column(String(2083), nullable=True)
    total_work_price = Column(Float, nullable=True)
    total_subventions = Column(Float, nullable=True)
    remaining_costs = Column(Float, nullable=True)
    subvention_on_TTC = Column(Integer, nullable=True)
    total_advances = Column(Float, nullable=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=True)

    @hybrid_property
    def quotes(self):
        # Return all duplicated quotes linked to the simulation
        return [
            simulation_quote.base_quote for simulation_quote in self.simulation_quotes
        ]

    @hybrid_property
    def funders(self):
        # Return all duplicated funders linked to the simulation
        return [
            {
                "simulation_funder_id": simulation_funder.id,
                "funder": simulation_funder.duplicate_funder,
                "scenario": simulation_funder.match_scenario,
                "rate": simulation_funder.rate,
                "advance": simulation_funder.advance,
                "subventioned_expense": simulation_funder.subventioned_expense,
                "funder_accommodations": simulation_funder.funder_accommodations,
                "base_funder_id": simulation_funder.base_funder_id,
            }
            for simulation_funder in self.simulation_funders
        ]

    @hybrid_property
    def base_funders(self):
        # Return all base funders linked to the simulation
        return [
            {
                "funder": simulation_funder.base_funder,
            }
            for simulation_funder in self.simulation_funders
        ]

    @hybrid_property
    def deposit_funders(self):
        # Return all deposit funders linked to the simulation
        return [
            {
                "funder": deposit_funder.funder,
                "deposit_date": deposit_funder.deposit_date,
            }
            for deposit_funder in self.simulation_funders
        ]

    @hybrid_property
    def payment_request_funders(self):
        # Return all payment request funders linked to the simulation
        return [
            {
                "funder": payment_request_funder.funder,
                "payment_request_date": payment_request_funder.payment_request_date,
            }
            for payment_request_funder in self.payment_request_funders
        ]

    @hybrid_property
    def certification_funders(self):
        # Return all certification funders linked to the simulation
        return [
            {
                "funder": certification_funder.funder,
                "certification_date": certification_funder.certification_date,
            }
            for certification_funder in self.certification_funders
        ]

    @hybrid_property
    def is_frozen(self):
        for use_case in self.use_cases:
            if use_case.use_case_name in SIMULATIONS_USE_CASES:
                return True
        return False


class SimulationUseCase(BaseMixin, db.Model):
    """SimulationUseCase"""

    __tablename__ = "simulation_use_case"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    use_case_name = Column(String(255), nullable=False)
    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=True)
    simulation = relationship(
        "Simulation", backref=backref("use_cases", cascade="all, delete-orphan")
    )
