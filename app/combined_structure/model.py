from sqlalchemy import (
    Column,
    Date,
    Integer,
    Text,
    ForeignKey,
    String,
    Boolean,
    Float,
    BigInteger,
)
from sqlalchemy.orm import relationship
from app.copro.president import President
from app import db
from app.common.base_model import BaseMixin, SoftDeletableMixin


class CombinedStructure(SoftDeletableMixin, BaseMixin, db.Model):
    __tablename__ = "combined_structure"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    mission = relationship("Mission", backref="combined_structures")
    # generalites
    name = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    currently_working_on = Column(Boolean(), nullable=True)
    nb_lots = Column(Integer(), nullable=True)
    nb_copros = Column(Integer(), nullable=True)
    creation_year = Column(Integer(), nullable=True)
    other_objects_linked = Column(Boolean(), nullable=True)
    other_objects_linked_details = Column(Text(), nullable=True)
    # syndic et president
    president_id = Column(Integer, ForeignKey("president.id"), nullable=False)
    president = relationship("President", backref="combined_structures")
    members_cs = Column(Text(), nullable=True)
    # gestion fonctionnement
    annual_budget = Column(Float())
    last_general_assemblee_date = Column(Date(), nullable=True)
    account_closing_date = Column(Date(), nullable=True)
    main_member_exists = Column(Boolean(), nullable=True)
    main_member = Column(Text(), nullable=True)
    rules_exists = Column(Boolean(), nullable=True)
    total_tantieme = Column(BigInteger(), nullable=True)
    # contrats
    contract_syndic = Column(Boolean(), nullable=True)
    contract_syndic_date = Column(String(), nullable=True)
    contract_green_spaces = Column(Boolean(), nullable=True)
    contract_green_spaces_date = Column(String(), nullable=True)
    contract_heater = Column(Boolean(), nullable=True)
    contract_heater_date = Column(String(), nullable=True)
    contract_trash_room = Column(Boolean(), nullable=True)
    contract_trash_room_date = Column(String(), nullable=True)
    contract_trash_management = Column(Boolean(), nullable=True)
    contract_trash_management_date = Column(String(), nullable=True)
    contract_lodge = Column(Boolean(), nullable=True)
    contract_lodge_date = Column(String(), nullable=True)
    contract_aerial_parking = Column(Boolean(), nullable=True)
    contract_aerial_parking_date = Column(String(), nullable=True)
    contract_underground_parking = Column(Boolean(), nullable=True)
    contract_underground_parking_date = Column(String(), nullable=True)
    contract_cctv = Column(Boolean(), nullable=True)
    contract_cctv_date = Column(String(), nullable=True)
    other_technical_equipments = Column(Boolean(), nullable=True)
    # commentaires / precisions
    comment = Column(Text(), nullable=True)
