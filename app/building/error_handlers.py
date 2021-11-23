from .controller import api
from .exceptions import BuildingNotFoundException
from ..common.error_handlers import parse_exception


@api.errorhandler(BuildingNotFoundException)
def building_not_found(error):  # pragma: no cover
    return parse_exception(error)
