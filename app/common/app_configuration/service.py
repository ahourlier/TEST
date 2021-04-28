from . import AppConfig
from .exceptions import AppConfigNotFoundException


class AppConfigService:
    @staticmethod
    def get_by_id(app_config_id: str) -> str:
        db_app_config = AppConfig.query.get(app_config_id)
        return db_app_config

    @staticmethod
    def get_by_key(app_config_key: str) -> str:
        db_app_config = AppConfig.query.filter(AppConfig.key == app_config_key).first()
        return db_app_config
