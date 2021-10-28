from typing import List

from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from .error_handlers import ReferentNotFoundException

# from .exceptions import ChildReferentMissionException
from .interface import ReferentInterface
from .model import Referent, Referent
from app.admin.error_handlers import InconsistentUpdateIdException

# from ...common.exceptions import ChildMissionException
# from ...common.phone_number.model import PhoneNumber
# from ...common.phone_number.service import PhoneNumberService
# from ...common.search import sort_query

from app import db
from .schema import ReferentSchema

CLIENTS_DEFAULT_PAGE = 1
CLIENTS_DEFAULT_PAGE_SIZE = 100
CLIENTS_DEFAULT_SORT_FIELD = "id"
CLIENTS_DEFAULT_SORT_DIRECTION = "desc"


class ReferentService:
    @staticmethod
    def get_all() -> List[Referent]:
        return ReferentSchema().dump(
            Referent.query.filter(Referent.active == True).all(), many=True
        )

    @staticmethod
    def get_by_id(referent_id: int) -> Referent:
        db_referent = Referent.query.get(referent_id)
        if db_referent is None or not db_referent.active:
            raise ReferentNotFoundException
        return db_referent

    @staticmethod
    def create(new_attrs: ReferentInterface) -> Referent:
        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
                del new_attrs["phone_number"]
        new_referent = Referent(**new_attrs)
        db.session.add(new_referent)
        db.session.commit()
        return new_referent

    @staticmethod
    def update(referent: Referent, changes: ReferentInterface) -> Referent:
        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    referent, [changes.get("phone_number")]
                )
            del changes["phone_number"]
        referent.update(changes)
        db.session.commit()
        return referent

    @staticmethod
    def has_changed(referent: Referent, changes: ReferentInterface) -> bool:
        for key, value in changes.items():
            if getattr(referent, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(referent_id: int) -> int or None:
        referent = Referent.query.filter(Referent.id == referent_id).first()
        if not referent:
            raise ReferentNotFoundException
        # if referent.missions:
        #     A mission depends of this referent. Must not be deleted.
        # raise ChildReferentMissionException
        referent.active = False
        db.session.commit()
        return referent_id
