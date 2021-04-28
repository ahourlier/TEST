from sqlalchemy import Column, Integer, String
from app import db
from app.common.base_model import BaseMixin


class AppConfig(BaseMixin, db.Model):
    """ Application Configuration table """

    __tablename__ = "app_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False)
    value = Column(String(800), nullable=False)
