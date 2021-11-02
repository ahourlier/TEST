from app import db
from sqlalchemy import Column, String


class Subjob(db.Model):

    __tablename__ = "subjob"

    value = Column(String(255), primary_key=True)
