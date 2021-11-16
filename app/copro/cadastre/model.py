from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app import db
from app.common.base_model import BaseMixin


class Cadastre(BaseMixin, db.Model):
    __tablename__ = "cadastre"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    copro_id = Column(Integer, ForeignKey("copro.id"), nullable=False)
    value = Column(String(255), nullable=False)
    copro = relationship("Copro", backref="cadastres")
