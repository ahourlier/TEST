from enum import Enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class EmailStatus(Enum):
    TO_SEND = "A envoyer"
    SENT = "Envoyé"
    ERROR = "Erreur"


class Email(BaseMixin, db.Model):
    """ Email  """

    __tablename__ = "email"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    subject = Column(String(980), nullable=True)
    to = Column(ARRAY(String(255), dimensions=1), nullable=True)
    cc = Column(ARRAY(String(255), dimensions=1), nullable=True)
    bcc = Column(ARRAY(String(255), dimensions=1), nullable=True)
    content = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default=EmailStatus.TO_SEND.value)
    project_ids = Column(ARRAY(Integer, dimensions=1), nullable=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    sender = relationship("User", backref=backref("sent_emails"))
    sent_date = Column(DateTime, nullable=True)
    attachments = Column(ARRAY(String(100), dimensions=1), nullable=True)
    error = Column(Text, nullable=True)
