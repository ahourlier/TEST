from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.common.address.model import Address
from app.common.app_name import App
from app.common.search import sort_query
from app.copro.cadastre import Cadastre
from app.copro.copros.exceptions import CoproNotFoundException, MissionNotTypeCoproException
from app.copro.copros.interface import CoproInterface
from app.copro.copros.model import Copro
from app.mission.missions.service import MissionService

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

    @staticmethod
    def create(new_attrs: CoproInterface) -> Copro:

        mission = MissionService.get_by_id(new_attrs.get("mission_id"))
        if mission.mission_type != App.COPRO:
            raise MissionNotTypeCoproException

        cadastres = None
        if new_attrs.get('cadastres'):
            cadastres = new_attrs.get('cadastres')
            del new_attrs['cadastres']

        new_copro = Copro(**new_attrs)
        db.session.add(new_copro)
        db.session.commit()

        if cadastres:
            for c in cadastres:
                c['copro_id'] = new_copro.id
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

        return new_copro

    @staticmethod
    def get(copro_id) -> Copro:
        db_copro = Copro.query.get(copro_id)

        if db_copro is None:
            raise CoproNotFoundException

        return db_copro

    @staticmethod
    def update(db_copro: Copro, changes: CoproInterface, copro_id: int) -> Copro:

        if changes.get("cadastres"):
            delete_cadastres = Cadastre.__table__.delete().where(Cadastre.copro_id == copro_id)
            db.session.execute(delete_cadastres)
            db.session.commit()

            for c in changes.get("cadastres"):
                new_cadastre = Cadastre(**c)
                db.session.add(new_cadastre)
                db.session.commit()

            del changes["cadastres"]

        db_copro.update(changes)
        db.session.commit()

        return db_copro

    @staticmethod
    def delete(copro_id: int):
        current_copro = CoproService.get(copro_id)
        if current_copro:
            current_copro.soft_delete()
            db.session.commit()
        return copro_id
