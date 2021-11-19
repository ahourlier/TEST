from sqlalchemy import Boolean, String, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.address.model import Address
from app.common.base_model import SoftDeletableMixin, BaseMixin
from app.copro.cadastre import Cadastre
from app.copro.president import President


class Copro(SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "copro"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="copros")
    president_id = Column(Integer, ForeignKey("president.id"), nullable=True)
    president = relationship("President", backref="copro")
    moe_id = Column(Integer, ForeignKey("moe.id"), nullable=True)
    moe = relationship("Moe", backref="copro")
    # copropriété
    name = Column(String(255), nullable=True)
    copro_type = Column(String(255), nullable=True)
    address_1_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address_1 = relationship(
        "Address",
        cascade="all, delete",
        passive_deletes=True,
        foreign_keys=[address_1_id],
        primaryjoin=address_1_id == Address.id,
    )
    address_2_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address_2 = relationship(
        "Address",
        cascade="all, delete",
        passive_deletes=True,
        foreign_keys=[address_2_id],
        primaryjoin=address_2_id == Address.id,
    )
    user_in_charge_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user_in_charge = relationship("User", backref="copro")
    mixed_copro = Column(Boolean, nullable=True, default=False)
    priority_copro = Column(Boolean, nullable=True, default=False)
    horizontal_copro = Column(Boolean, nullable=True, default=False)
    copro_registry_number = Column(Integer, nullable=True)
    copro_creation_date = Column(db.Date, nullable=True)
    is_member_s1_s2 = Column(Boolean, nullable=True, default=False)
    is_member_association = Column(Boolean, nullable=True, default=False)
    # association = Column(String(255), nullable=True) # TODO link to ASL
    # Fonctionnement
    nb_lots = Column(Integer, nullable=True)
    nb_co_owners = Column(Integer, nullable=True)
    nb_sub_lots = Column(Integer, nullable=True)
    percentage_lots_to_habitation = Column(Float, nullable=True)
    percentage_tantiemes_to_habitation = Column(Float, nullable=True)
    contract_end_date = Column(db.Date, nullable=True)
    closing_accounts_date = Column(db.Date, nullable=True)
    last_assembly_date = Column(db.Date, nullable=True)
    percentage_attending_tantiemes = Column(Float, nullable=True)
    percentage_attending_co_owners = Column(Float, nullable=True)
    institutional_landlords_presence = Column(Boolean, nullable=True, default=False)
    # charges
    charges_last_year = Column(Float, nullable=True)
    provisional_budget_last_assembly = Column(Float, nullable=True)
    average_charges_per_quarter_per_lot = Column(Float, nullable=True)
    # description technique rapide
    construction_time = Column(String(255), nullable=True)
    pmr = Column(Boolean, nullable=True, default=False)
    igh = Column(Boolean, nullable=True, default=False)
    external_spaces = Column(Boolean, nullable=True, default=False)
    underground_parking = Column(Boolean, nullable=True, default=False)
    aerial_parking = Column(Boolean, nullable=True, default=False)
