from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class TaxableIncome(BaseMixin, db.Model):
    """Taxable Income"""

    __tablename__ = "taxable_income"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    date = db.Column(Integer(), nullable=True)
    income = db.Column(Integer(), nullable=True)
    requester_id = Column(Integer, ForeignKey("requester.id"), nullable=False)
    requester = relationship(
        "Requester", backref=backref("taxable_incomes", cascade="all,delete")
    )
