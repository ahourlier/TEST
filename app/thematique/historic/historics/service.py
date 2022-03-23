from distutils.version import Version
from app import db
from app.thematique.historic.historics import Historic
from app.thematique.historic.historics.exceptions import HistoricNotFoundException
from app.thematique.historic.historics.interface import HistoricInterface
from app.thematique.error_handlers import (
    VersionNotFoundException
)
from app.thematique.historic.historics.error_handlers import (
    CreateHistoricException,
    HistoricNotFoundException
)
from app.thematique.service import ThematiqueService

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
        try:
            # Check thematique exists in Firestore
            ThematiqueService.get_version(new_attrs['thematique_id'])
        except VersionNotFoundException as ve:
            print(f"{ve.message}")
            raise CreateHistoricException
        new_historic = Historic(**new_attrs)
        db.session.add(new_historic)
        if commit:
            db.session.commit()
        return new_historic

    @staticmethod
    def delete_by_id(historic_id: int, commit: bool = False) -> int:
        db_historic = Historic.query.get(historic_id)
        if not db_historic:
            raise HistoricNotFoundException
        db_historic.soft_delete()
        if commit:
            db.session.commit()
        return historic_id