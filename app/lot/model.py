from sqlalchemy import Column, Integer, Text, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import SoftDeletableMixin, BaseMixin


class Building(SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "lot"

    id = Column(Integer(), primary_key=True, autoincrement=True)

    copro_id = Column(Integer, ForeignKey("copro.id"), nullable=False)
    copro = relationship("Copro", backref="buildings")

    building_id = Column(Integer, ForeignKey("building.id"), nullable=True)
    building = relationship("Building", backref="lots")
    # informations
    lot_number = Column(Integer)
    type = Column(String(255))
    owner_status = Column(String(255))
    # tantieme et surface
    habitation_type = Column(String(255))
    floor = Column(String(255))
    door = Column(String(255))
    surface = Column(Float)
    status_if_habitation = Column(String(255))
    occupant_status = Column(String(255))
    cave_surface = Column(Float)
    balcony_surface = Column(Float)
    # impayes
    unpaid_amount = Column(Float)
    unpaid_date = Column(db.Date)
    # Pour les logements loues, niveau de loyer
    lease_type = Column(String(255))
    rent_per_month = Column(String(255))
    charges_per_month = Column(String(255))
    intermediate_rent = Column(Boolean)
    convention_rent_type = Column(String(255))
    # suivi des dia
    dia = Column(Boolean)
    dia_price = Column(Float)
    dia_price_m2 = Column(Float)
