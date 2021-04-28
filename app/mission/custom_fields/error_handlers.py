from . import api
from app.common.error_handlers import parse_exception
from .exceptions import (
    CustomFieldNotFoundException,
    AvailableFieldValueNotFoundException,
)


@api.errorhandler(CustomFieldNotFoundException)
def custom_field_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(AvailableFieldValueNotFoundException)
def available_field_not_found(error):  # pragma: no cover
    return parse_exception(error)
