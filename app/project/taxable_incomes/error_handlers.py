from . import api
from .exceptions import TaxableIncomeNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(TaxableIncomeNotFoundException)
def taxable_income_not_found(error):  # pragma: no cover
    return parse_exception(error)
