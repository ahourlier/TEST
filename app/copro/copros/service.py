from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app.common.address.model import Address
from app.common.search import sort_query
from app.copro.copros.model import Copro

COPRO_DEFAULT_PAGE = 1
COPRO_DEFAULT_PAGE_SIZE = 20
COPRO_DEFAULT_SORT_FIELD = "created_at"
COPRO_DEFAULT_SORT_DIRECTION = "desc"


class CoproService:

    @staticmethod
    def get_all(
            page=COPRO_DEFAULT_PAGE,
            size=COPRO_DEFAULT_PAGE_SIZE,
            term=None,
            sort_by=COPRO_DEFAULT_SORT_FIELD,
            direction=COPRO_DEFAULT_SORT_DIRECTION,
            mission_id=None,
    ) -> Pagination:
        import app.mission.permissions as mission_permissions

        q = sort_query(Copro.query, sort_by, direction)
        q = q.filter(or_(Copro.is_deleted == False, Copro.is_deleted == None))
        if term is not None:
            search_term = f"%{term}%"
            q = q.join(Address).filter(
                or_(
                    Copro.name.ilike(search_term),
                    Address.full_address.ilike(search_term),
                )
            )

        if mission_id is not None:
            q = q.filter(Copro.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)
