from sqlalchemy import select, Boolean, String, Column, Integer, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.address.model import Address
from app.common.base_model import SoftDeletableMixin, BaseMixin
from app.common.phone_number.model import PhoneNumber, HasPhones
from app.copro.cadastre import Cadastre
from app.copro.president import President
from app.copro.moe import Moe


class Copro(HasPhones, SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "copro"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="copros")
    president_id = Column(Integer, ForeignKey("president.id"), nullable=True)
    president = relationship("President", backref="copro")
    moe_id = Column(Integer, ForeignKey("moe.id"), nullable=True)
    moe = relationship("Moe", backref="copro")

    # syndic
    syndic_name = Column(String(255), nullable=True)
    syndic_type = Column(String(255), nullable=True)
    syndic_contract_date = Column(Date, nullable=True)
    syndic_manager_name = Column(String(255), nullable=True)
    syndic_manager_email = Column(String(255), nullable=True)
    syndic_comment = Column(Text(), nullable=True)
    syndic_manager_address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    syndic_manager_address = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[syndic_manager_address_id],
        primaryjoin=syndic_manager_address_id == Address.id,
    )

    admin_name = Column(String(255), nullable=True)
    admin_type = Column(String(255), nullable=True)
    admin_contract_date = Column(Date, nullable=True)
    admin_manager_name = Column(String(255), nullable=True)
    admin_manager_email = Column(String(255), nullable=True)
    admin_comment = Column(Text(), nullable=True)
    admin_manager_address_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    admin_manager_address = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[admin_manager_address_id],
        primaryjoin=admin_manager_address_id == Address.id,
    )

    # copropriété
    name = Column(String(255), nullable=True)
    copro_type = Column(String(255), nullable=True)
    address_1_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address_1 = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[address_1_id],
        primaryjoin=address_1_id == Address.id,
    )
    address_2_id = Column(Integer(), ForeignKey("address.id"), nullable=True)
    address_2 = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[address_2_id],
        primaryjoin=address_2_id == Address.id,
    )
    user_in_charge_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user_in_charge = relationship("User", backref="copro")
    mixed_copro = Column(Boolean, nullable=True, default=False)
    priority_copro = Column(Boolean, nullable=True, default=False)
    horizontal_copro = Column(Boolean, nullable=True, default=False)
    copro_registry_number = Column(String(255), nullable=True)
    copro_creation_date = Column(db.Date, nullable=True)
    is_member_s1_s2 = Column(Boolean, nullable=True, default=False)
    is_member_association = Column(Boolean, nullable=True, default=False)
    # combined structure
    cs_id = Column(Integer, ForeignKey("combined_structure.id"), nullable=True)
    cs = relationship("CombinedStructure", backref="copros")
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

    @hybrid_property
    def syndic_manager_phone_number(self):
        return self.phones[0] if self.phones else None

    @syndic_manager_phone_number.expression
    def syndic_manager_phone_number(cls):
        return select([PhoneNumber]).where(PhoneNumber.resource_id == cls.id).first()

    @hybrid_property
    def admin_manager_phone_number(self):
        return self.phones[1] if self.phones else None

    @admin_manager_phone_number.expression
    def admin_manager_phone_number(cls):
        return select([PhoneNumber]).where(
            PhoneNumber.resource_id == cls.id
        ).order_by(
            PhoneNumber.id.desc()
        ).first()