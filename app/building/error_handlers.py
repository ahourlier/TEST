from . import api
from .exceptions import BuildingNotFoundException, WrongConstructionTimeException, WrongERPCategoryException, \
    WrongAccessTypeException, WrongCollectiveHeaterException, WrongAsbestosDiagnosisResultException
from ..common.error_handlers import parse_exception


@api.errorhandler(BuildingNotFoundException)
def building_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongConstructionTimeException)
def wrong_construction_time(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongERPCategoryException)
def wrong_erp_category(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongAccessTypeException)
def wrong_access_type(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongCollectiveHeaterException)
def wrong_collective_heater(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(WrongAsbestosDiagnosisResultException)
def wrong_asbestos_diagnosis_result(error):  # pragma: no cover
    return parse_exception(error)
