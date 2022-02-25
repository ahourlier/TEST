
from app.common.search import sort_query
from app.v2_imports import Imports


IMPORT_DEFAULT_PAGE = 1
IMPORT_DEFAULT_PAGE_SIZE = 100
IMPORT_DEFAULT_SORT_FIELD = "id"
IMPORT_DEFAULT_SORT_DIRECTION = "asc"

class ImportsService:
    
    
    def list(
        page=IMPORT_DEFAULT_PAGE,
        size=IMPORT_DEFAULT_PAGE_SIZE,
        sort_by=IMPORT_DEFAULT_SORT_FIELD,
        direction=IMPORT_DEFAULT_SORT_DIRECTION,
        mission_id=None,
    ):
        q = sort_query(
            Imports.query,
            sort_by,
            direction,
        )

        if mission_id:
            q = q.filter(Imports.mission_id == mission_id)
        
        return q.paginate(page=page, per_page=size)