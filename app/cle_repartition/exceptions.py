from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    CLE_REPARTITION_NOT_FOUND_EXCEPTION,
    KEY_CLE_REPARTITION_NOT_FOUND_EXCEPTION,
)


class CleRepartitionNotFoundException(HTTPException):
    def __init__(self, message=CLE_REPARTITION_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_CLE_REPARTITION_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
