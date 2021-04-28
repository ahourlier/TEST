from . import api
from .exceptions import UserNotFoundException, UnknownConnexionEmail, InactiveUser
from app.common.error_handlers import parse_exception


@api.errorhandler(UserNotFoundException)
def user_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(UnknownConnexionEmail)
def unknown_connexion_email(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(InactiveUser)
def inactive_user(error):  # pragma: no cover
    return parse_exception(error)
