import logging

from flask import g
from flask_sqlalchemy import Pagination
from sqlalchemy import or_

from app import db
from app.auth.users.model import UserRole
from app.common.exceptions import InconsistentUpdateIdException, ForbiddenException
from app.common.phone_number.model import PhoneNumber
from app.common.phone_number.service import PhoneNumberService
from app.common.search import sort_query
from app.project.accommodations import Accommodation
from app.project.accommodations.error_handlers import AccommodationNotFoundException
from app.project.accommodations.interface import AccommodationInterface
import app.project.disorders.service as disorders_service
import app.project.projects.service as projects_service
import app.project.taxable_incomes.service as taxable_incomes_service
from app.project.projects import Project

ACCOMMODATIONS_DEFAULT_PAGE = 1
ACCOMMODATIONS_DEFAULT_PAGE_SIZE = 100
ACCOMMODATIONS_DEFAULT_SORT_FIELD = "id"
ACCOMMODATIONS_DEFAULT_SORT_DIRECTION = "desc"


class AccommodationService:
    @staticmethod
    def get_all(
        page=ACCOMMODATIONS_DEFAULT_PAGE,
        size=ACCOMMODATIONS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=ACCOMMODATIONS_DEFAULT_SORT_FIELD,
        direction=ACCOMMODATIONS_DEFAULT_SORT_DIRECTION,
        project_id=None,
    ) -> Pagination:
        q = sort_query(Accommodation.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(or_(Accommodation.name.ilike(search_term),))

        if project_id is None and g.user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            raise ForbiddenException()

        if project_id is not None:
            q = q.filter(Accommodation.project_id == project_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def create(
        new_attrs: AccommodationInterface, project_id: int = None
    ) -> Accommodation:
        """ Create a new accommodation with its disorders """
        accommodation_fields = AccommodationInterface(**new_attrs)
        if "disorders" in accommodation_fields:
            del accommodation_fields["disorders"]

        # Project link
        if project_id is not None:
            projects_service.ProjectService.get_by_id(project_id)
            accommodation_fields["project_id"] = project_id

        # Create phone number
        if "phone_number" in accommodation_fields:
            if accommodation_fields.get("phone_number", None):
                accommodation_fields["phones"] = [
                    PhoneNumber(**accommodation_fields.get("phone_number"))
                ]
            del accommodation_fields["phone_number"]

        accommodation = Accommodation(**accommodation_fields)
        db.session.add(accommodation)
        db.session.commit()
        logging.info(f"Accommodation created {accommodation}")

        # Create linked disorders
        if "disorders" in new_attrs:
            disorders_service.DisorderService.create_list(
                new_attrs.get("disorders"), accommodation_id=accommodation.id
            )

        return accommodation

    @staticmethod
    def get_by_id(accommodation_id: str) -> Accommodation:
        db_accommodation = Accommodation.query.get(accommodation_id)
        if db_accommodation is None:
            raise AccommodationNotFoundException()
        return db_accommodation

    @staticmethod
    def update(
        accommodation: Accommodation,
        changes: AccommodationInterface,
        force_update: bool = False,
    ) -> Accommodation:
        if force_update or AccommodationService.has_changed(accommodation, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != accommodation.id:
                raise InconsistentUpdateIdException()

            # Update disorders
            disorders_service.DisorderService.update_list(
                changes["disorders"], accommodation_id=accommodation.id
            )
            del changes["disorders"]

            # Update phone number
            if "phone_number" in changes:
                if changes.get("phone_number", None):
                    PhoneNumberService.update_phone_numbers(
                        accommodation, [changes.get("phone_number")], commit=True
                    )
                del changes["phone_number"]
            accommodation.update(changes)
            db.session.commit()
        return accommodation

    @staticmethod
    def has_changed(
        accommodation: Accommodation, changes: AccommodationInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(accommodation, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(accommodation_id: int) -> int or None:
        accommodation = Accommodation.query.filter(
            Accommodation.id == accommodation_id
        ).first()
        if not accommodation:
            raise AccommodationNotFoundException
        db.session.delete(accommodation)
        db.session.commit()
        return accommodation_id
