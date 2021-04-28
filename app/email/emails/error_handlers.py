from . import api
from .exceptions import (
    EmailNotFoundException,
    EmailMissingRecipientException,
    EmailNotInternalSenderException,
)
from app.common.error_handlers import parse_exception


@api.errorhandler(EmailNotFoundException)
def email_not_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(EmailMissingRecipientException)
def email_missing_recipient_found(error):  # pragma: no cover
    return parse_exception(error)


@api.errorhandler(EmailNotInternalSenderException)
def email_not_internal_sender_exception(error):  # pragma: no cover
    return parse_exception((error))
