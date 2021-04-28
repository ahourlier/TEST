from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    AGENCY_NOT_FOUND_EXCEPTION,
    KEY_AGENCY_NOT_FOUND_EXCEPTION,
    CHILD_ANTENNA_EXCEPTION,
    KEY_CHILD_ANTENNA_EXCEPTION,
    AGENCY_DUPLICATE_NAME_EXCEPTION,
    KEY_AGENCY_DUPLICATE_NAME_EXCEPTION,
    CHILD_AGENCY_MISSION_EXCEPTION,
    KEY_CHILD_AGENCY__MISSION_EXCEPTION,
)


class AgencyNotFoundException(HTTPException):
    def __init__(self, message=AGENCY_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_AGENCY_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class AgencyDuplicateNameException(HTTPException):
    def __init__(self, message=AGENCY_DUPLICATE_NAME_EXCEPTION):
        self.code = 400
        self.key = KEY_AGENCY_DUPLICATE_NAME_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ChildAntennaException(HTTPException):
    def __init__(self, message=CHILD_ANTENNA_EXCEPTION):
        self.code = 400
        self.key = KEY_CHILD_ANTENNA_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class ChildAgencyMissionException(HTTPException):
    def __init__(self, message=CHILD_AGENCY_MISSION_EXCEPTION):
        self.code = 400
        self.key = KEY_CHILD_AGENCY__MISSION_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
