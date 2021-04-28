from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.common.base_model import BaseMixin


class AppEnum(BaseMixin, db.Model):
    """ Table for all enums """

    __tablename__ = "enum"

    kind = Column(String(255), nullable=False, primary_key=True)
    name = Column(String(500), nullable=False, primary_key=True)
    display_order = Column(Integer)
    disabled = Column(Boolean, nullable=False, default=False)
    private = Column(Boolean, nullable=False, default=False)


class PerrenoudEnum(BaseMixin, db.Model):
    """ Table for all Perrenoud enums """

    __tablename__ = "perrenoud_enum"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    index = Column(Integer(), nullable=False)
    value = Column(Integer(), nullable=False)
    label = Column(String(255), nullable=False)


class PerrenoudEnumKind(BaseMixin, db.Model):
    """ Map index/labels for Perrenoud enums"""

    __tablename__ = "perrenoud_enum_kind"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    index = Column(Integer(), nullable=False)
    label = Column(String(255), nullable=True)
