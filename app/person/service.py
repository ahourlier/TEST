from sqlalchemy import or_, and_

from flask import g

from app import db
from app.common.address.model import Address
from app.common.address.service import AddressService
from app.auth.users.service import UserService
from app.common.exceptions import EnumException
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.person import Person
from app.lot import Lot
from app.person.model import LotOwner
from app.person.error_handlers import (
    PersonNotFoundException,
    EnumException as PersonEnumException,
)
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
    def create(changes: PersonInterface, user_email=None):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise PersonEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        if "phone_number" in changes:
            if changes.get("phone_number", None):
                changes["phones"] = [PhoneNumber(**changes.get("phone_number"))]
            del changes["phone_number"]

        address_id = None
        if "address" in changes and changes.get("address") is not None:
            address_id = AddressService.create_address(changes.get("address"))
            del changes["address"]

        new_person = Person(**changes)

        if address_id:
            new_person.address_id = address_id

        db_user = None
        # Defined when running Cloud task calling this method
        if user_email is not None:
            db_user = UserService.get_by_email(user_email)
        else:
            db_user = g.user

        if db_user is not None:
            if db_user.groups and len(db_user.groups) > 0:
                antenna_id = None
                for group in db_user.groups:
                    antenna_id = group.antenna.id
                if antenna_id is not None:
                    new_person.antenna_id = antenna_id
        else:
            print(
                "Creating a person: no user found with this email: Skipping antenna_id setup"
            )
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
        if term not in [None, ""]:
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
                enum=e.details.get("enum"),
            )

        if "phone_number" in changes:
            PhoneNumberService.update_phone_numbers(
                db_person,
                [changes.get("phone_number")],
            )
            del changes["phone_number"]

        if "address" in changes:
            if changes.get("address") is not None:
                if not db_person.address_id:
                    db_person.address_id = AddressService.create_address(
                        changes.get("address")
                    )
                else:
                    db_address = Address.query.get(db_person.address_id)
                    db_address.update(changes.get("address"))
            else:
                address = Address.query.filter(Address.id == db_person.address_id)
                db_person.address_id = None
                address.delete()
            del changes["address"]

        db_person.update(changes)
        db.session.commit()
        return db_person

    @staticmethod
    def delete(person_id: int):
        db_person = PersonService.get(person_id)
        db_person.soft_delete()
        db.session.commit()
        return person_id

    @staticmethod
    def search_person_by_address_and_name(address_obj, lastname, firstname):
        try:
            found_person = (
                Person.query.join(Address, Person.address_id == Address.id)
                .filter(
                    and_(
                        Address.number == str(address_obj.get("number")),
                        Address.street == str(address_obj.get("street")),
                        Address.postal_code == str(address_obj.get("postal_code")),
                        Address.city == str(address_obj.get("city")),
                        Person.first_name == firstname,
                        Person.last_name == lastname,
                        Person.is_deleted == False,
                    )
                )
                .first()
            )
            return found_person
        except Exception as e:
            print(e)

    def search_person_by_name_and_is_owner_in_lot(
        existing_lot, lastname, firstname, company_name
    ):
        # Get all person with specified lastname / firstname or lastname / company_name
        persons = Person.query.filter(
            or_(
                and_(Person.last_name == lastname, Person.first_name == firstname),
                and_(Person.last_name == lastname, Person.company_name == company_name),
            )
        )
        # Check for each found person if it is an owner in current lot
        for person in persons:
            for existing_owner in existing_lot.owners:
                if person.id == existing_owner.id:
                    # When found a match, return the existing owner
                    return person

    def remove_owners_from_lot(existing_lot):
        for owner in existing_lot.owners:
            # Remove all existing owners from existing lot
            stmt = LotOwner.delete().where(
                (
                    LotOwner.c.owner_id == owner.id
                    and LotOwner.c.lot_id == existing_lot.id
                )
            )
            db.session.execute(stmt)
        db.session.commit()
