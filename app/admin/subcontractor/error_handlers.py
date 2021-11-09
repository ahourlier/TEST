from . import api
from .exceptions import SubcontractorNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(SubcontractorNotFoundException)
def subcontractor_not_found(error):  # pragma: no cover
    return parse_exception(error)
