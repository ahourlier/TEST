from .scenarios import api
from .photos import api as photos_api
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidFileException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)


@photos_api.errorhandler(InvalidFileException)
def invalid_filename(error):  # pragma: no cover
    return parse_exception(error)
