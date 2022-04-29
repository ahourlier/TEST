from sqlalchemy import Column, String, Integer, ForeignKey, Enum as sqlAlchemyEnum
from sqlalchemy.orm import relationship

from enum import Enum

from app import db
from app.common.base_model import BaseMixin


class Role(BaseMixin, db.Model):
    """User Role"""

    __tablename__ = "role"
    name = Column(String(255), nullable=False, primary_key=True)
    value = Column(Integer, nullable=False, default=0)


class VersionType(Enum):
    V1 = "INDIVIDUEL"
    V2 = "COPROPRIETE"


class Permission(BaseMixin, db.Model):
    """Permission Matrix"""

    __tablename__ = "permission"

    entity = Column(String(255), nullable=False, primary_key=True)
    action = Column(String(255), nullable=False, primary_key=True)
    applied_to = Column(sqlAlchemyEnum(VersionType), nullable=False, primary_key=True)
    role_id = Column(
        String(255), ForeignKey("role.name"), nullable=False, primary_key=True
    )
    role = relationship("Role", backref="permissions")
