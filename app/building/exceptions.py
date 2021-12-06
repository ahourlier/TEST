from werkzeug.exceptions import HTTPException
from app.common.config_error_messages import (
    BUILDING_NOT_FOUND_EXCEPTION,
    KEY_BUILDING_NOT_FOUND_EXCEPTION, WRONG_CONSTRUCTION_TIME_EXCEPTION, KEY_WRONG_CONSTRUCTION_TIME_EXCEPTION,
    WRONG_ERP_CATEGORY_EXCEPTION, KEY_WRONG_ERP_CATEGORY_EXCEPTION, KEY_WRONG_ACCESS_TYPE_EXCEPTION,
    WRONG_ACCESS_TYPE_EXCEPTION, WRONG_COLLECTIVE_HEATER_EXCEPTION, KEY_WRONG_COLLECTIVE_HEATER_EXCEPTION,
    WRONG_ASBESTOS_DIAGNOSIS_RESULT_EXCEPTION, KEY_WRONG_ASBESTOS_DIAGNOSIS_RESULT_EXCEPTION
)


class BuildingNotFoundException(HTTPException):
    def __init__(self, message=BUILDING_NOT_FOUND_EXCEPTION):
        super().__init__(description=message)
        self.code = 404
        self.key = KEY_BUILDING_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"


class WrongConstructionTimeException(HTTPException):
    def __init__(self, message=WRONG_CONSTRUCTION_TIME_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_CONSTRUCTION_TIME_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongERPCategoryException(HTTPException):
    def __init__(self, message=WRONG_ERP_CATEGORY_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_ERP_CATEGORY_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongAccessTypeException(HTTPException):
    def __init__(self, message=WRONG_ACCESS_TYPE_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_ACCESS_TYPE_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongCollectiveHeaterException(HTTPException):
    def __init__(self, message=WRONG_COLLECTIVE_HEATER_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_COLLECTIVE_HEATER_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"


class WrongAsbestosDiagnosisResultException(HTTPException):
    def __init__(self, message=WRONG_ASBESTOS_DIAGNOSIS_RESULT_EXCEPTION):
        super().__init__(description=message)
        self.code = 400
        self.key = KEY_WRONG_ASBESTOS_DIAGNOSIS_RESULT_EXCEPTION
        self.message = message
        self.status = "BAD REQUEST"
