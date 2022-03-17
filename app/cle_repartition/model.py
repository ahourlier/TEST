from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    select,
    ForeignKey,
    Table,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


class LotCleRepartition(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id = Column(Integer, ForeignKey("lot.id"), nullable=False)
    cle_repartition_id = Column(
        Integer, ForeignKey("cle_repartition.id"), nullable=False
    )
    tantieme = Column(Float, nullable=False)
    lot = relationship("Lot", backref="cles_repartition")
    cle_repartition = relationship("CleRepartition")


class CleRepartition(BaseMixin, db.Model):
    """Represents a cle_repartition"""

    __tablename__ = "cle_repartition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255), nullable=False)
    copro_id = Column(Integer, ForeignKey("copro.id"), nullable=False)
    copro = relationship(
        "Copro", backref=backref("cles_repartition", cascade="all, delete"),
    )
