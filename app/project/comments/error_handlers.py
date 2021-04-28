from . import api
from .exceptions import CommentNotFoundException
from app.common.error_handlers import parse_exception


@api.errorhandler(CommentNotFoundException)
def comment_not_found(error):  # pragma: no cover
    return parse_exception(error)
