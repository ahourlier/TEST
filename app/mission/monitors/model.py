from sqlalchemy import Column, INTEGER, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship, backref

from app import db
from app.common.base_model import BaseMixin


DEFAULT_FIELDS = '[{"type":"date", "name":"Dépôt", "default": true, "automatic":true}, {"type":"date", "name":"Agrément", "default": true, "automatic":true}, {"type":"date", "name":"Avance", "default": true, "automatic":false},{"type":"boolean", "name":"Avance - Demande de prorogation", "default": true, "automatic":false},{"type":"date", "name":"Acompte 1", "default": true, "automatic":false}, {"type":"date", "name":"Acompte 2", "default": true, "automatic":false}, {"type":"date", "name":"Réception pièces paiement", "default": true, "automatic":false}, {"type":"date", "name":"Envoi demande de paiement", "default": true, "automatic":true}, {"type":"date", "name":"Paiement du solde", "default": true, "automatic":false}, {"type":"boolean", "name":"Paiement - Demande de prorogation", "default": true, "automatic":false}]'


class Monitor(BaseMixin, db.Model):
    """Monitors"""

    __tablename__ = "monitor"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=True)
    mission = relationship("Mission", backref=backref("monitor", uselist=False))
    advance_alert = Column(Integer(), nullable=True)
    payment_alert = Column(Integer(), nullable=True)
    commentary = Column(String(800), nullable=True)


class MonitorField(BaseMixin, db.Model):
    """MonitorsFields"""

    __tablename__ = "monitor_field"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    monitor_id = Column(Integer, ForeignKey("monitor.id"), nullable=True)
    monitor = relationship(
        "Monitor", backref=backref("fields", order_by="asc(MonitorField.id)")
    )
    type = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    invisible = Column(Boolean, nullable=True, default=False)
    default = Column(Boolean, nullable=True, default=False)
    automatic = Column(Boolean, nullable=True, default=False)
