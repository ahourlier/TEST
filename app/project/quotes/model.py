from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class QuoteAccommodation(BaseMixin, db.Model):
    """QuoteAccommodation"""

    __tablename__ = "quote_accommodation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    quote_id = Column(Integer, ForeignKey("quote.id"), nullable=True)
    quote = relationship(
        "Quote",
        foreign_keys="QuoteAccommodation.quote_id",
        backref="quotes_accommodations",
    )
    accommodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=True)
    accommodation = relationship("Accommodation", backref="accommodations_quotes")
    price_excl_tax = Column(Float(), nullable=True)
    price_incl_tax = Column(Float(), nullable=True)
    eligible_amount = Column(Float(), nullable=True)


class Quote(BaseMixin, db.Model):
    """Quote"""

    __tablename__ = "quote"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    is_bill = Column(Boolean, nullable=True)
    name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    company_origin = Column(String(255), nullable=True)
    precision = Column(String(255), nullable=True)
    price_excl_tax = Column(Float(), nullable=True)
    price_incl_tax = Column(Float(), nullable=True)
    eligible_amount = Column(Float(), nullable=True)
    note = Column(String(2083), nullable=True)
    common_price_excl_tax = Column(Float(), nullable=True)
    common_price_incl_tax = Column(Float(), nullable=True)
    common_eligible_amount = Column(Float(), nullable=True)
    common_note = Column(String(2083), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    project = relationship("Project", backref="quotes")

    @hybrid_property
    def is_used(self):
        return len(self.simulation_base_quotes) != 0

    @hybrid_property
    def is_frozen(self):
        freezing_use_cases = ["Dépôt", "Dossier agréé", "Paiement"]
        for simulation_base_quote in self.simulation_base_quotes:
            for use_case in simulation_base_quote.simulation.use_cases:
                if use_case.use_case_name in freezing_use_cases:
                    return True
        return False

    @hybrid_property
    def simulations(self):
        from app.project.simulations.model import Simulation
        from app.project.simulations.model import SimulationQuote

        return (
            Simulation.query.filter(
                Simulation.simulation_quotes.any(
                    SimulationQuote.base_quote_id == self.id
                )
            )
            .distinct()
            .all()
        )

    @hybrid_property
    def accommodations(self):
        # Return all accommodations linked to this quote
        return [
            {
                "quote_accommodation_id": quote_accommodation.id,
                "price_excl_tax": quote_accommodation.price_excl_tax,
                "price_incl_tax": quote_accommodation.price_incl_tax,
                "eligible_amount": quote_accommodation.eligible_amount,
                "accommodation": quote_accommodation.accommodation,
            }
            for quote_accommodation in self.quotes_accommodations
        ]


class QuoteWorkType(BaseMixin, db.Model):
    """QuoteWorkType"""

    __tablename__ = "quote_work_type"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    type_name = Column(String(255), nullable=False)
    quote_id = Column(Integer, ForeignKey("quote.id"), nullable=True)
    quote = relationship(
        "Quote", backref=backref("work_types", cascade="all, delete-orphan")
    )
