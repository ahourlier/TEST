import logging


def parse_exception(error):  # pragma: no cover
    logging.error(error.message)
    return (
        {"key": error.key, "status": error.status, "message": error.message},
        error.code,
    )
