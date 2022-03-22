from app import db
from app.thematique.historic.historics import Historic
from app.thematique.historic.historics.interface import HistoricInterface

HISTORICS_DEFAULT_PAGE = 1
HISTORICS_DEFAULT_PAGE_SIZE = 5
HISTORICS_DEFAULT_SORT_FIELD = "updated_at"
HISTORICS_DEFAULT_SORT_DIRECTION = "desc"

class HistoricService:
    @staticmethod
    def get_all(
        page=HISTORICS_DEFAULT_PAGE,
        size=HISTORICS_DEFAULT_PAGE_SIZE,
        sort_by=HISTORICS_DEFAULT_SORT_FIELD,
        direction=HISTORICS_DEFAULT_SORT_DIRECTION,
    ):
        col = getattr(Historic, sort_by)
        q = Historic.query.order_by(col.desc() if direction == "desc" else col.asc())
        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(new_attrs: HistoricInterface, commit: bool = False) -> Historic:
        #TODO: Check that template ID exists
        #TODO: Add associated exceptions
        new_historic = Historic(**new_attrs)
        db.session.add(new_historic)
        if commit:
            db.session.commit()
        return new_historic