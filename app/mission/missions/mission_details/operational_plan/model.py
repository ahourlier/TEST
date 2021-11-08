from app import db
from sqlalchemy import Column, String


class OperationalPlan(db.Model):

    __tablename__ = "operational_plan"

    value = Column(String(255), primary_key=True)
