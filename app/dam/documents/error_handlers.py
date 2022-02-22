from . import api
from .exceptions import DocumentNotFoundException, InvalidSourceException
from app.common.error_handlers import parse_exception
from app.common.exceptions import SharedDriveException

@api.errorhandler(DocumentNotFoundException)
def document_not_found(error):  # pragma: no cover
    return parse_exception(error)

@api.errorhandler(SharedDriveException)
def shared_drive_exception(error):  # pragma: no cover
    return parse_exception(error)

@api.errorhandler(InvalidSourceException)
def invalid_source_found(error):  # pragma: no cover
    return parse_exception(error)
