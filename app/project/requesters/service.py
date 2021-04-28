import logging

from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.auth.users.model import UserRole
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidSearchFieldException,
)
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.common.search import sort_query
from app.mission.missions import Mission
from app.mission.teams import Team
from app.project.projects import Project
from app.project.requesters import Requester
from app.project.requesters.error_handlers import RequesterNotFoundException
from app.project.requesters.exceptions import RequesterTypeConstantException
from app.project.requesters.interface import RequesterInterface
import app.project.contacts.service as contacts_service
import app.project.taxable_incomes.service as taxable_incomes_service
from app.project.requesters.model import RequesterTypes

REQUESTERS_DEFAULT_PAGE = 1
REQUESTERS_DEFAULT_PAGE_SIZE = 20
REQUESTERS_DEFAULT_SORT_FIELD = "created_at"
REQUESTERS_DEFAULT_SORT_DIRECTION = "desc"


class RequesterService:
    @staticmethod
    def get_all(
        page=REQUESTERS_DEFAULT_PAGE,
        size=REQUESTERS_DEFAULT_PAGE_SIZE,
        term=None,
        first_name=None,
        last_name=None,
        sort_by=REQUESTERS_DEFAULT_SORT_FIELD,
        direction=REQUESTERS_DEFAULT_SORT_DIRECTION,
        type=None,
        user=None,
        excluded_project=None,
    ) -> Pagination:
        q = sort_query(Requester.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Requester.email.ilike(search_term),
                    Requester.last_name.ilike(search_term),
                    Requester.first_name.ilike(search_term),
                )
            )
        if last_name:
            search_term = f"%{last_name}%"
            q = q.filter(Requester.last_name.ilike(search_term))
        if first_name:
            search_term = f"%{first_name}%"
            q = q.filter(Requester.first_name.ilike(search_term))

        # Filter by type
        if type is not None and type not in RequesterTypes.__members__:
            raise InvalidSearchFieldException()
        if type is not None:
            q = q.filter(Requester.type == RequesterTypes[type].value)

        # Check current user permissions for the projects list
        if user is not None and user.role != UserRole.ADMIN:
            user_agencies = [
                group.agency_id for group in user.groups if group.agency_id
            ]
            user_antennas = [
                group.antenna_id for group in user.groups if group.antenna_id
            ]
            q = q.filter(
                Requester.project.has(
                    Project.mission.has(
                        Mission.teams.any(
                            or_(
                                Team.user_id == user.id,
                                Team.antenna_id.in_(user_antennas),
                                Team.agency_id.in_(user_agencies),
                            )
                        )
                    )
                )
            )

        if excluded_project:
            try:
                q = q.filter(Requester.project.has(Project.id != int(excluded_project)))
            except ValueError:
                logging.error(
                    f"'excluded_project' params not a valid integer : {excluded_project}. No requester was excluded from the response"
                )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(requester_id: str) -> Requester:
        db_requester = Requester.query.get(requester_id)
        if db_requester is None:
            raise RequesterNotFoundException
        return db_requester

    @staticmethod
    def create(new_attrs: dict) -> Requester:
        """ Create a new requester, with its contacts and taxable_incomes """
        requester_fields = RequesterInterface(**new_attrs)
        del requester_fields["contacts"]
        del requester_fields["taxable_incomes"]

        phones = []
        if "phone_number_1" in requester_fields:
            if requester_fields.get("phone_number_1", None):
                phones.append(PhoneNumber(**requester_fields.get("phone_number_1")))
            del requester_fields["phone_number_1"]
        if "phone_number_2" in requester_fields:
            if requester_fields.get("phone_number_2", None):
                phones.append(PhoneNumber(**requester_fields.get("phone_number_2")))
            del requester_fields["phone_number_2"]
        requester_fields["phones"] = phones

        requester = Requester(**requester_fields)
        db.session.add(requester)
        db.session.flush()
        # Create linked contacts
        contacts_service.ContactService.create_list(
            new_attrs.get("contacts"), requester.id
        )
        # Create linked taxable_incomes
        taxable_incomes_service.TaxableIncomeService.create_list(
            new_attrs.get("taxable_incomes"), requester.id
        )
        return requester

    @staticmethod
    def update(
        requester: Requester, changes: RequesterInterface, force_update: bool = False
    ) -> Requester:
        if force_update or RequesterService.has_changed(requester, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != requester.id:
                raise InconsistentUpdateIdException()
            if changes.get("type") != requester.type:
                raise RequesterTypeConstantException()

            # Update phones numbers
            phones = []
            if "phone_number_1" in changes:
                if changes["phone_number_1"] is not None:
                    phones.append(changes.get("phone_number_1"))
                del changes["phone_number_1"]
            if "phone_number_2" in changes:
                if changes["phone_number_2"] is not None:
                    phones.append(changes.get("phone_number_2"))
                del changes["phone_number_2"]
            PhoneNumberService.update_phone_numbers(requester, phones)

            # Update contacts
            contacts_service.ContactService.update_list(
                changes["contacts"], requester.id
            )
            # Update taxable incomes
            taxable_incomes_service.TaxableIncomeService.update_list(
                changes["taxable_incomes"], requester.id
            )
            del changes["contacts"]
            del changes["taxable_incomes"]

            requester.update(changes)
            db.session.commit()
        return requester

    @staticmethod
    def has_changed(requester: Requester, changes: RequesterInterface) -> bool:
        for key, value in changes.items():
            if getattr(requester, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(requester_id: int) -> int or None:
        requester = Requester.query.filter(Requester.id == requester_id).first()
        if not requester:
            raise RequesterNotFoundException()
        db.session.delete(requester)
        db.session.commit()
        return requester_id
