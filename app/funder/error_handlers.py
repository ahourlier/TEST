from .funders import api
from app.common.exceptions import InconsistentUpdateIdException, ValidationException
from app.common.error_handlers import parse_exception


@api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(ValidationException)
def validation_exception(error):
    return parse_exception(error)
