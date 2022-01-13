from sqlalchemy import or_
from flask import g

from app import db
from app.common.exceptions import EnumException
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.person import Person
from app.person.error_handlers import PersonNotFoundException, EnumException as PersonEnumException
from app.person.interface import PersonInterface


PERSON_DEFAULT_PAGE = 1
PERSON_DEFAULT_PAGE_SIZE = 100
PERSON_DEFAULT_SORT_FIELD = "id"
PERSON_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "status": {"enum_key": "PersonStatus"},
}


class PersonService:
    @staticmethod
    def get(person_id: int) -> Person:
        person = Person.query.get(person_id)
        if not person or person.is_deleted:
            raise PersonNotFoundException
        return person

    @staticmethod
    def create(new_attrs: PersonInterface):

        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise PersonEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if "phone_number" in new_attrs:
            if new_attrs.get("phone_number", None):
                new_attrs["phones"] = [PhoneNumber(**new_attrs.get("phone_number"))]
            del new_attrs["phone_number"]

        new_person = Person(**new_attrs)
        if g.user.groups and len(g.user.groups) > 0:
            antenna_id = None
            for group in g.user.groups:
                antenna_id = group.antenna.id
            if antenna_id is not None:
                new_person.antenna_id = antenna_id
        db.session.add(new_person)
        db.session.commit()
        return new_person

    @staticmethod
    def get_all(
        page=PERSON_DEFAULT_PAGE,
        size=PERSON_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=PERSON_DEFAULT_SORT_FIELD,
        direction=PERSON_DEFAULT_SORT_DIRECTION,
        antenna_id=None,
    ):
        q = sort_query(
            Person.query.filter(
                or_(Person.is_deleted == False, Person.is_deleted == None)
            ),
            sort_by,
            direction,
        )
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Person.first_name.ilike(search_term),
                    Person.last_name.ilike(search_term),
                    Person.email_address.ilike(search_term),
                )
            )

        if antenna_id:
            q = q.filter(Person.antenna_id == antenna_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def update(db_person: Person, changes: PersonInterface):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise PersonEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum")
            )

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                PhoneNumberService.update_phone_numbers(
                    db_person, [changes.get("phone_number")]
                )
            del changes["phone_number"]

        db_person.update(changes)
        db.session.commit()
        return db_person

    @staticmethod
    def delete(person_id: int):
        db_person = PersonService.get(person_id)
        db_person.soft_delete()
        db.session.commit()
        return person_id
