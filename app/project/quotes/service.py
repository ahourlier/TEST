from typing import List

from flask import g
from flask_sqlalchemy import Pagination
from sqlalchemy import or_, not_

from app import db
from app.common.exceptions import InconsistentUpdateIdException, ForbiddenException
from app.common.search import sort_query
from app.project.quotes import Quote
from app.project.quotes.error_handlers import (
    QuoteNotFoundException,
    WorkTypeNotFoundException,
    QuoteAccommodationNotFoundException,
)
from app.project.quotes.interface import (
    QuoteInterface,
    QuoteWorkTypeInterface,
)
import app.project.projects.service as project_service
import app.project.accommodations.service as accommodations_service
from app.project.quotes.model import QuoteWorkType, QuoteAccommodation

QUOTES_DEFAULT_PAGE = 1
QUOTES_DEFAULT_PAGE_SIZE = 100
QUOTES_DEFAULT_SORT_FIELD = "id"
QUOTES_DEFAULT_SORT_DIRECTION = "desc"


class QuoteService:
    @staticmethod
    def get_all(
        page=QUOTES_DEFAULT_PAGE,
        size=QUOTES_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=QUOTES_DEFAULT_SORT_FIELD,
        direction=QUOTES_DEFAULT_SORT_DIRECTION,
        project_id=None,
    ) -> Pagination:
        q = sort_query(Quote.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Quote.name.ilike(search_term),
                    Quote.company.ilike(search_term),
                )
            )

        if project_id is not None:
            q = q.filter(Quote.project_id == project_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(quote_id: str) -> Quote:
        db_quote = Quote.query.get(quote_id)
        if db_quote is None:
            raise QuoteNotFoundException
        return db_quote

    @staticmethod
    def create(new_attrs: QuoteInterface) -> Quote:
        """Create a new quote in a given project"""
        work_types = None
        accommodations = None
        # Check if project exist
        project_service.ProjectService.get_by_id(new_attrs.get("project_id"))
        # Check if work_types exist and save them :
        if "work_types" in new_attrs and new_attrs.get("work_types"):
            work_types = new_attrs.get("work_types")
            del new_attrs["work_types"]
        if new_attrs.get("accommodations") and new_attrs.get("accommodations"):
            accommodations = new_attrs.get("accommodations")
            del new_attrs["accommodations"]
        # Create new quote
        quote = Quote(**new_attrs)

        db.session.add(quote)
        db.session.commit()
        # Create work_types :
        if work_types:
            QuoteWorkTypeService.create_list(work_types, quote.id)
        # Create accommodations
        if accommodations:
            QuoteAccommodationService.create_update_list(accommodations, quote.id)

        return quote

    @staticmethod
    def update(
        quote: Quote, changes: QuoteInterface, force_update: bool = False
    ) -> Quote:
        if force_update or QuoteService.has_changed(quote, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != quote.id:
                raise InconsistentUpdateIdException()
            quote = QuoteService.set_simulation_flag(quote, changes)
            # Update work types
            if "work_types" in changes:
                QuoteWorkTypeService.update_list(changes.get("work_types"), quote.id)
                del changes["work_types"]
            # Update accommodations
            if "accommodations" in changes:
                QuoteAccommodationService.create_update_list(
                    changes.get("accommodations"), quote.id
                )
                del changes["accommodations"]
            # Update quote
            quote.update(changes)
            db.session.commit()
        return quote

    @staticmethod
    def set_simulation_flag(quote: Quote, changes: QuoteInterface) -> Quote:
        """If one or many quotes linked to a simulation have been modified
        (within the fields specified as MODIFICATORS_FIELDS below),
        the "quotes_modified" must be updated, so the user can be informed of the modification"""
        MODIFICATORS_FIELDS = [
            "name",
            "price_excl_tax",
            "price_incl_tax",
            "eligible_amount",
        ]
        quote_modified = False
        for field in MODIFICATORS_FIELDS:
            if field in changes and changes[field] != getattr(quote, field):
                quote_modified = True
                break
        # Work types must be analysed apart, because they are nested children
        if "work_types" in changes:
            changes_types_names = [
                work_type["type_name"] for work_type in changes["work_types"]
            ]
            quote_types_names = [work_type.type_name for work_type in quote.work_types]
            changes_types_names.sort()
            quote_types_names.sort()
            if changes_types_names != quote_types_names:
                quote_modified = True

        if quote_modified:
            for simulation_quote in quote.simulation_base_quotes:
                simulation_quote.simulation.quotes_modified = True

        return quote

    @staticmethod
    def has_changed(quote: Quote, changes: QuoteInterface) -> bool:
        for key, value in changes.items():
            if getattr(quote, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(quote_id: int) -> int or None:
        quote = Quote.query.filter(Quote.id == quote_id).first()
        if not quote:
            raise QuoteNotFoundException
        db.session.delete(quote)
        db.session.commit()
        return quote_id


class QuoteWorkTypeService:
    @staticmethod
    def get_by_id(work_type_id: str) -> QuoteWorkType:
        db_quote_work_type = QuoteWorkType.query.get(work_type_id)
        if db_quote_work_type is None:
            raise WorkTypeNotFoundException
        return db_quote_work_type

    @staticmethod
    def create(new_attrs: QuoteWorkTypeInterface) -> QuoteWorkType:
        QuoteService.get_by_id(new_attrs.get("quote_id"))
        work_type = QuoteWorkType(**new_attrs)
        db.session.add(work_type)
        db.session.commit()
        return work_type

    @staticmethod
    def duplicate(work_type_id: str, new_parent_id: str):
        base_wt = QuoteWorkTypeService.get_by_id(work_type_id)
        duplicate_dict = base_wt.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(duplicate_dict):
            if key not in base_wt.__table__.columns.keys():
                del duplicate_dict[key]
        # Remove auto_generated values :
        del duplicate_dict["id"]
        del duplicate_dict["updated_at"]
        del duplicate_dict["created_at"]
        # Replace parent quote id :
        duplicate_dict["quote_id"] = new_parent_id
        duplicate_wt = QuoteWorkTypeService.create(
            QuoteWorkTypeInterface(**duplicate_dict)
        )
        return duplicate_wt

    @staticmethod
    def create_list(
        work_types_values: List[QuoteWorkTypeInterface],
        quote_id: int,
    ) -> List[QuoteWorkType]:

        work_types = []
        # Create corresponding work types
        for work_type in work_types_values:
            work_type["quote_id"] = quote_id
            work_types.append(QuoteWorkTypeService.create(work_type))
        return work_types

    @staticmethod
    def update_list(work_types_fields, quote_id):
        # Delete
        old_work_types = QuoteWorkType.query.filter(
            QuoteWorkType.quote_id == quote_id
        ).all()
        for old_work_type in old_work_types:
            QuoteWorkTypeService.delete_by_id(old_work_type.id)

        work_types = []
        # Re-create
        for wt in work_types_fields:
            wt["quote_id"] = quote_id
            work_types.append(QuoteWorkTypeService.create(wt))

        return work_types

    @staticmethod
    def delete_by_id(work_type_id: int) -> int or None:
        work_type = QuoteWorkType.query.filter(QuoteWorkType.id == work_type_id).first()
        if not work_type:
            raise WorkTypeNotFoundException
        db.session.delete(work_type)
        db.session.commit()
        return work_type_id


class QuoteAccommodationService:
    @staticmethod
    def create(quote_id: str, new_attrs) -> QuoteAccommodation:
        """
        Create a new QuoteAccommodation relationship
        """
        QuoteService.get_by_id(quote_id)
        new_attrs["quote_id"] = quote_id
        accommodations_service.AccommodationService.get_by_id(
            new_attrs["accommodation"]["id"]
        )
        new_attrs["accommodation_id"] = new_attrs["accommodation"]["id"]
        del new_attrs["accommodation"]
        quote_accommodation = QuoteAccommodation(**new_attrs)
        db.session.add(quote_accommodation)
        db.session.commit()
        return quote_accommodation

    @staticmethod
    def update(
        quote_accommodation: QuoteAccommodation, changes, force_update: bool = False
    ) -> QuoteAccommodation:
        # Remove "accommodation" key. We don't update that.
        if "accommodation" in changes:
            del changes["accommodation"]
        # "quote_accommodation_id" does not exist into the model.
        if "quote_accommodation_id" in changes:
            del changes["quote_accommodation_id"]
        if force_update or QuoteAccommodationService.has_changed(
            quote_accommodation, changes
        ):
            quote_accommodation.update(changes)
            db.session.commit()
        return quote_accommodation

    @staticmethod
    def create_update_list(quotes_accommodations_fields, quote_id):
        quote = QuoteService.get_by_id(quote_id)
        original_quotes_id = [
            quote_accommodation.id
            for quote_accommodation in quote.quotes_accommodations
        ]
        changes_qa_id = [
            quote_accommodation_field["quote_accommodation_id"]
            for quote_accommodation_field in quotes_accommodations_fields
            if "quote_accommodation_id" in quote_accommodation_field
        ]

        for quote_accommodation_field in quotes_accommodations_fields:
            # Create
            if "quote_accommodation_id" not in quote_accommodation_field:
                QuoteAccommodationService.create(
                    quote_id, quote_accommodation_field.copy()
                )
            # Update
            else:
                quote_accommodation = QuoteAccommodationService.get_by_id(
                    quote_accommodation_field["quote_accommodation_id"]
                )
                QuoteAccommodationService.update(
                    quote_accommodation, quote_accommodation_field.copy()
                )

        # Delete obsolete quotes associations
        for original_id in original_quotes_id:
            if original_id not in changes_qa_id:
                QuoteAccommodationService.delete_by_id(original_id)

        return quote.quotes_accommodations

    @staticmethod
    def get_by_id(quote_accommodation_id: str) -> QuoteAccommodation:
        db_quote_accommodation = QuoteAccommodation.query.get(quote_accommodation_id)
        if db_quote_accommodation is None:
            raise QuoteAccommodationNotFoundException()
        return db_quote_accommodation

    @staticmethod
    def has_changed(quote_accommodation: QuoteAccommodation, changes) -> bool:
        for key, value in changes.items():
            if getattr(quote_accommodation, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(quote_accommodation_id: int) -> int or None:
        q = QuoteAccommodation.query.filter_by(id=quote_accommodation_id)
        if not q.scalar():
            raise QuoteAccommodationNotFoundException
        q.delete()
        db.session.commit()
        return quote_accommodation_id
