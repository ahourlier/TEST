from app import db
from sqlalchemy import Column, String


class Job(db.Model):

    __tablename__ = "job"

    value = Column(String(255), primary_key=True)
