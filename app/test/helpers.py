from typing import List

from flask_sqlalchemy import Pagination


def make_pagination(
    items: List = None, page: int = 1, per_page: int = 20, total: int = 0
) -> Pagination:
    """ Creates a pagination object for testing search apis """
    results = items if items else []
    return Pagination(
        query=None, page=page, per_page=per_page, total=total, items=results
    )
