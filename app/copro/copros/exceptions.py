from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    COPRO_NOT_FOUND_EXCEPTION,
    KEY_COPRO_NOT_FOUND_EXCEPTION,
    MISSION_NOT_TYPE_COPRO_EXCEPTION,
    KEY_MISSION_NOT_TYPE_COPRO_EXCEPTION,
    WRONG_COPRO_TYPE_EXCEPTION,
    KEY_WRONG_COPRO_TYPE_EXCEPTION_EXCEPTION,
    WRONG_CONSTRUCTION_TIME_EXCEPTION,
    KEY_WRONG_CONSTRUCTION_TIME_EXCEPTION,
)


class CoproNotFoundException(HTTPException):
    def __init__(self, message=COPRO_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_COPRO_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class MissionNotTypeCoproException(HTTPException):
    def __init__(self, message=MISSION_NOT_TYPE_COPRO_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_MISSION_NOT_TYPE_COPRO_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongCoproTypeException(HTTPException):
    def __init__(self, message=WRONG_COPRO_TYPE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_COPRO_TYPE_EXCEPTION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongConstructionTimeException(HTTPException):
    def __init__(self, message=WRONG_CONSTRUCTION_TIME_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_CONSTRUCTION_TIME_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
