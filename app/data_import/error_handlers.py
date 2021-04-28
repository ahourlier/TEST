from . import data_import_api
from .exceptions import (
    DataImportNotFoundException,
    IncorrectDataImportException,
    EntityInsertFailException,
)
from ..common.error_handlers import parse_exception
from ..common.exceptions import InconsistentUpdateIdException


@data_import_api.errorhandler(InconsistentUpdateIdException)
def inconsistent_update_id(error):  # pragma: no cover
    return parse_exception(error)


@data_import_api.errorhandler(DataImportNotFoundException)
def data_import_not_found(error):  # pragma: no cover
    return parse_exception(error)


@data_import_api.errorhandler(IncorrectDataImportException)
def incorrect_data_import(error):  # pragma: no cover
    return parse_exception(error)


@data_import_api.errorhandler(EntityInsertFailException)
def entity_insert_fail(error):  # pragma: no cover
    return parse_exception(error)
