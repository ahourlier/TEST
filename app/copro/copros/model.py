from sqlalchemy import (
    select,
    Boolean,
    String,
    Column,
    Integer,
    ForeignKey,
    Float,
    Date,
    Text,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.address.model import Address
from app.common.base_model import SoftDeletableMixin, BaseMixin
from app.common.phone_number.model import PhoneNumber, HasPhones


class Copro(HasPhones, SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "copro"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="copros")
    president_id = Column(Integer, ForeignKey("president.id"), nullable=True)
    president = relationship("President", backref="copro")
    moe_id = Column(Integer, ForeignKey("moe.id"), nullable=True)
    moe = relationship("Moe", backref="copro")
    # combined structure
    cs_id = Column(Integer, ForeignKey("combined_structure.id"), nullable=True)
    cs = relationship("CombinedStructure", backref="copros")

    # copropriété
    name = Column(String(255), nullable=True)
    copro_type = Column(String(255), nullable=True)
    access_code = Column(Text(), nullable=True)

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

    # syndic & CS
    syndic_name = Column(String(255), nullable=True)
    syndic_type = Column(String(255), nullable=True)
    syndic_contract_date = Column(Date, nullable=True)
    syndic_manager_name = Column(String(255), nullable=True)
    syndic_manager_email = Column(String(255), nullable=True)
    syndic_comment = Column(Text(), nullable=True)
    syndic_manager_address_id = Column(
        Integer(), ForeignKey("address.id"), nullable=True
    )
    syndic_manager_address = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[syndic_manager_address_id],
        primaryjoin=syndic_manager_address_id == Address.id,
    )

    admin_name = Column(String(255), nullable=True)
    admin_contract_date = Column(Date, nullable=True)
    admin_manager_name = Column(String(255), nullable=True)
    admin_manager_email = Column(String(255), nullable=True)
    admin_comment = Column(Text(), nullable=True)
    admin_manager_address_id = Column(
        Integer(), ForeignKey("address.id"), nullable=True
    )
    admin_manager_address = relationship(
        "Address",
        cascade="all, delete",
        foreign_keys=[admin_manager_address_id],
        primaryjoin=admin_manager_address_id == Address.id,
    )
    other_syndic_counsel_member_infos = Column(Text(), nullable=True)

    # Personnel
    caretaker_id = Column(Integer(), ForeignKey("caretaker.id"), nullable=True)
    caretaker = relationship("CareTaker", backref="copro")
    employee_id = Column(Integer(), ForeignKey("employee.id"), nullable=True)
    employee = relationship("Employee", backref="copro")
    fire_safety_personnel_id = Column(
        Integer(), ForeignKey("fire_safety_personnel.id"), nullable=True
    )
    fire_safety_personnel = relationship("FireSafetyPersonnel", backref="copro")

    # Architecte conseil
    architect_id = Column(Integer(), ForeignKey("architect.id"), nullable=True)
    architect = relationship("Architect", backref="copro")

    # Fonctionnement
    nb_lots = Column(Integer, nullable=True)
    nb_co_owners = Column(Integer, nullable=True)
    nb_commercial_lots = Column(Integer, nullable=True)
    nb_sub_lots = Column(Integer, nullable=True)
    percentage_lots_to_habitation = Column(Float, nullable=True)
    percentage_tantiemes_to_habitation = Column(Float, nullable=True)
    po_majority = Column(Boolean, nullable=True)
    institutional_landlords_presence = Column(Boolean, nullable=True, default=False)

    # description technique rapide
    nb_building = Column(Integer, nullable=True)
    construction_time = Column(String(255), nullable=True)
    pmr = Column(Boolean, nullable=True, default=False)
    igh = Column(Boolean, nullable=True, default=False)
    collective_heating = Column(Boolean, nullable=True)
    rcu = Column(Boolean, nullable=True)
    heritage_classification = Column(Boolean, nullable=True)
    external_spaces = Column(Boolean, nullable=True, default=False)
    nb_aerial_parking_spaces = Column(Integer(), nullable=True)
    nb_underground_parking_spaces = Column(Integer(), nullable=True)
    
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
        return (
            select([PhoneNumber])
            .where(PhoneNumber.resource_id == cls.id)
            .order_by(PhoneNumber.id.desc())
            .first()
        )
