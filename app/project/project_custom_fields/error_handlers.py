from . import api
from app.common.error_handlers import parse_exception
from .exceptions import (
    ProjectCustomFieldNotFoundException,
    CustomFieldValueNotFoundException,
)


@api.errorhandler(ProjectCustomFieldNotFoundException)
def project_custom_field_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(CustomFieldValueNotFoundException)
def custom_field_value_not_found(error):  # pragma: no cover
    return parse_exception(error)
