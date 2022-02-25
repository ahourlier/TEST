import imp
from sqlalchemy import Column, Integer, Text, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship

from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin
from app.copro.copros.model import Copro


class Building(SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "building"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    copro_id = Column(Integer, ForeignKey("copro.id"), nullable=False)
    copro = relationship("Copro", backref="buildings")
    # batiment
    name = Column(String(255), nullable=False)
    address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", backref="building")
    # contact
    referents = Column(Text(), nullable=True)
    # generalites du batiment
    construction_time = Column(String(255), nullable=True)
    igh = Column(Boolean(), nullable=True)
    r_plus = Column(String(255), nullable=True)
    r_minus = Column(String(255), nullable=True)
    erp = Column(Boolean(), nullable=True)
    erp_category = Column(String(255), nullable=True)
    last_security_commission_date = Column(db.Date, nullable=True)
    lodge = Column(Boolean(), nullable=True)
    nb_habitations_rcp = Column(Integer(), nullable=True)
    nb_habitations_noted = Column(Integer(), nullable=True)
    total_surface = Column(Float(), nullable=True)
    nb_annex_lots = Column(Integer(), nullable=True)
    nb_aerial_parking_spaces = Column(Integer(), nullable=True)
    nb_underground_parking_spaces = Column(Integer(), nullable=True)
    # acces
    access_type = Column(String(255), nullable=True)
    access_code = Column(Text(), nullable=True)
    access_type_cave = Column(String(255), nullable=True)
    access_type_roof = Column(String(255), nullable=True)
    # caracteristiques techniques
    lifts = Column(Integer(), nullable=True)
    roof = Column(String(255), nullable=True)
    vmc = Column(Boolean(), nullable=True)
    collective_heater = Column(String(255), nullable=True)
    ground_heating = Column(Boolean(), nullable=True)
    individual_cold_water_counter = Column(Boolean(), nullable=True)
    individual_ecs_counter = Column(Boolean(), nullable=True)
    other_equipments = Column(Text(), nullable=True)
    # diagnostique technique
    energy_diagnosis_date = Column(db.Date, nullable=True)
    initial_energy_label = Column(String(255), nullable=True)
    initial_consumption = Column(Float(), nullable=True)
    asbestos_diagnosis_date = Column(db.Date, nullable=True)
    asbestos_diagnosis_result = Column(String(255), nullable=True)
    lead_diagnosis_date = Column(db.Date, nullable=True)
    security_commission_date = Column(db.Date, nullable=True)
    security_commission_result = Column(Text(), nullable=True)
    other_technical_diagnosis = Column(Text(), nullable=True)
    # commentaires / precisions
    comment = Column(Text(), nullable=True)

