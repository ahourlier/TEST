from werkzeug.exceptions import HTTPException

from app.common.config_error_messages import (
    TAXABLE_INCOME_NOT_FOUND_EXCEPTION,
    KEY_TAXABLE_INCOME_NOT_FOUND_EXCEPTION,
)


class TaxableIncomeNotFoundException(HTTPException):
    def __init__(self, message=TAXABLE_INCOME_NOT_FOUND_EXCEPTION):
        self.code = 404
        self.key = KEY_TAXABLE_INCOME_NOT_FOUND_EXCEPTION
        self.message = message
        self.status = "NOT FOUND"
