from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    LOT_NOT_FOUND_EXCEPTION,
    KEY_LOT_NOT_FOUND_EXCEPTION,
    WRONG_ENUM_TYPE_EXCEPTION,
    KEY_INCORRECT_REPARTITION_KEY_EXCEPTION,
    INCORRECT_REPARTITION_KEY_EXCEPTION,
)


class LotNotFoundException(HTTPException):
    def __init__(self, message=LOT_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_LOT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class LotEnumException(HTTPException):
    def __init__(self, message=WRONG_ENUM_TYPE_EXCEPTION, value=None, enum=None):
        message.format(value=value, enum=enum)
        super().__init__(description=message)
        self.code = 400
        # self.key = KEY_LOT_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class IncorrectKeyException(HTTPException):
    def __init__(self, message=INCORRECT_REPARTITION_KEY_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_INCORRECT_REPARTITION_KEY_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
