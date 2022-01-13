import logging


def parse_exception(error):  # pragma: no cover
    logging.error(error.message)
    parsed = {"key": error.key, "status": error.status, "message": error.message}
    if hasattr(error, "details"):
        parsed["details"] = error.details
    return (
        parsed,
        error.code,
    )
