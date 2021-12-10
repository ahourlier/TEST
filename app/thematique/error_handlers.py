from .controller import api
from .exceptions import VersionNotFoundException
from ..common.error_handlers import parse_exception


@api.errorhandler(VersionNotFoundException)
def version_not_found(error):  # pragma: no cover
    return parse_exception(error)
