from app import db
from app.common.base_model import BaseMixin
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String


class FinancialDevice(BaseMixin, db.Model):

    # dispositif financiers mobilisés
    __tablename__ = "financial_device"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_details_id = Column(
        Integer(), ForeignKey("mission_detail.id"), nullable=False
    )
    mandate_account_type = Column(String(255), nullable=True)
    organization_funds_provider = Column(String(255), nullable=True)
    bank_account_name = Column(String(255), nullable=True)
    bank_name = Column(String(255), nullable=True)
    agreement_signature_date = Column(db.Date, nullable=True)
    amendment_signature_date = Column(db.Date, nullable=True)
    convention_number = Column(String(255), nullable=True)
    initiale_envelop = Column(Integer(), nullable=True)
    complementary_envelop = Column(Integer(), nullable=True)
    internal_audit_date = Column(db.Date, nullable=True)
    external_audit_date = Column(db.Date, nullable=True)
    funds_return_date = Column(db.Date, nullable=True)
    amount_returned = Column(Integer(), nullable=True)
    closing_date = Column(db.Date, nullable=True)
    transfer_circuit_validation = Column(String(500), nullable=True)
    operating_details = Column(String(500), nullable=True)