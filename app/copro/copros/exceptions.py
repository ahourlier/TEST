from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    COPRO_NOT_FOUND_EXCEPTION,
    KEY_COPRO_NOT_FOUND_EXCEPTION,
    MISSION_NOT_TYPE_COPRO_EXCEPTION,
    KEY_MISSION_NOT_TYPE_COPRO_EXCEPTION,
    REPARTITION_KEY_LINKED_EXCEPTION,
    KEY_REPARTITION_KEY_LINKED_EXCEPTION,
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


class RepartitionKeyLinkedException(HTTPException):
    def __init__(self, message=REPARTITION_KEY_LINKED_EXCEPTION):
        self.code = 400
        self.key = KEY_REPARTITION_KEY_LINKED_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
