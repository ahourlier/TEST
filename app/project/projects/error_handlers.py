from . import api
from .exceptions import ProjectNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(ProjectNotFoundException)
def project_not_found(error):  # pragma: no cover
    return parse_exception(error)
