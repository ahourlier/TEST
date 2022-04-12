from operator import or_
from typing import List

from flask_sqlalchemy import Pagination

from app import db
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidSearchFieldException,
)
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.mission.custom_fields import CustomField
from app.mission.custom_fields.error_handlers import CustomFieldNotFoundException
from app.mission.custom_fields.exceptions import AvailableFieldValueNotFoundException
from app.mission.custom_fields.interface import (
    CustomFieldInterface,
    AvailableFieldValueInterface,
)
import app.mission.missions.service as missions_service
from app.mission.custom_fields.model import FieldsCategories, AvailableFieldValue

CUSTOM_FIELDS_DEFAULT_PAGE = 1
CUSTOM_FIELDS_DEFAULT_PAGE_SIZE = 100
CUSTOM_FIELDS_DEFAULT_SORT_FIELD = "id"
CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION = "desc"


class CustomFieldService:
    @staticmethod
    def get_all(
        page=CUSTOM_FIELDS_DEFAULT_PAGE,
        size=CUSTOM_FIELDS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=CUSTOM_FIELDS_DEFAULT_SORT_FIELD,
        direction=CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        fetch_deleted=False,
        category=None,
    ) -> Pagination:
        q = sort_query(CustomField.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    CustomField.name.ilike(search_term),
                )
            )

        if mission_id is not None:
            q = q.filter(CustomField.mission_id == mission_id)

        if fetch_deleted == False:
            q = q.filter(
                or_(CustomField.is_deleted == False, CustomField.is_deleted == None)
            )

        # Filter by category
        if category is not None and category not in FieldsCategories.__members__:
            raise InvalidSearchFieldException()
        if category is not None:
            q = q.filter(CustomField.category == FieldsCategories[category].value)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(custom_field_id: str) -> CustomField:
        db_custom_field = CustomField.query.get(custom_field_id)
        if db_custom_field is None:
            raise CustomFieldNotFoundException
        return db_custom_field

    @staticmethod
    def create(new_attrs: CustomFieldInterface) -> CustomField:
        """Create a new custom_field associated to a mission"""
        if "mission_id" in new_attrs:
            missions_service.MissionService.get_by_id(new_attrs.get("mission_id"))

        extracted_fields = ServicesUtils.clean_attrs(new_attrs, ["available_values"])
        custom_field = CustomField(**new_attrs)
        db.session.add(custom_field)
        db.session.commit()

        # Create available values for this custom field
        if "available_values" in extracted_fields and extracted_fields.get(
            "available_values"
        ):
            AvailableFieldValueService.create_update_list(
                custom_field.id, extracted_fields.get("available_values")
            )

        return custom_field

    @staticmethod
    def update(
        custom_field: CustomField,
        changes: CustomFieldInterface,
        force_update: bool = False,
    ) -> CustomField:
        # Some values cannot be updated into custom_fields. We remove them first.
        ServicesUtils.clean_attrs(
            changes, ["category", "type", "is_multiple", "mission_id"]
        )
        if force_update or CustomFieldService.has_changed(custom_field, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != custom_field.id:
                raise InconsistentUpdateIdException()

            extracted_fields = ServicesUtils.clean_attrs(changes, ["available_values"])

            custom_field.update(changes)
            db.session.commit()

            # Updated available values for this custom field
            if "available_values" in extracted_fields and extracted_fields.get(
                "available_values"
            ):
                AvailableFieldValueService.create_update_list(
                    custom_field.id, extracted_fields.get("available_values")
                )

        return custom_field

    @staticmethod
    def has_changed(custom_field: CustomField, changes: CustomFieldInterface) -> bool:
        for key, value in changes.items():
            if getattr(custom_field, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(custom_field_id: int) -> int:
        custom_field = CustomField.query.filter(
            CustomField.id == custom_field_id
        ).first()
        if not custom_field:
            raise CustomFieldNotFoundException
        custom_field.soft_delete()
        db.session.commit()
        return custom_field_id


class AvailableFieldValueService:
    @staticmethod
    def get_by_id(available_field_value_id: str) -> AvailableFieldValue:
        db_available_field_value = AvailableFieldValue.query.get(
            available_field_value_id
        )
        if db_available_field_value is None:
            raise AvailableFieldValueNotFoundException()
        return db_available_field_value

    @staticmethod
    def create(
        new_attrs: AvailableFieldValueInterface, custom_field_id: None
    ) -> AvailableFieldValue:
        """Create a new available_field_value associated to a custom_field"""
        if custom_field_id is not None:
            new_attrs["custom_field_id"] = custom_field_id
        CustomFieldService.get_by_id(new_attrs.get("custom_field_id"))

        available_field_value = AvailableFieldValue(**new_attrs)
        db.session.add(available_field_value)
        db.session.commit()
        return available_field_value

    @staticmethod
    def update(
        available_field_value: AvailableFieldValue,
        changes: AvailableFieldValueInterface,
        force_update: bool = False,
    ) -> AvailableFieldValue:
        ServicesUtils.clean_attrs(changes, ["project_custom_field_id"])
        if force_update or AvailableFieldValueService.has_changed(
            available_field_value, changes
        ):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != available_field_value.id:
                raise InconsistentUpdateIdException()
            available_field_value.update(changes)
            db.session.commit()
        return available_field_value

    @staticmethod
    def create_update_list(custom_field_id, changes: List):
        custom_field = CustomFieldService.get_by_id(custom_field_id)
        original_available_field_values_id = [
            value.id for value in custom_field.available_values
        ]
        changes_afv_id = [
            available_value_fields["id"]
            for available_value_fields in changes
            if "id" in available_value_fields
        ]

        for available_value_fields in changes:
            # Create
            if "id" not in available_value_fields:
                AvailableFieldValueService.create(
                    available_value_fields.copy(), custom_field_id
                )
            # Update
            else:
                available_value = AvailableFieldValueService.get_by_id(
                    available_value_fields["id"]
                )
                AvailableFieldValueService.update(
                    available_value, available_value_fields.copy()
                )

        # Delete obsolete available_field_values
        for original_id in original_available_field_values_id:
            if original_id not in changes_afv_id:
                AvailableFieldValueService.delete_by_id(original_id)

        return custom_field.available_values

    @staticmethod
    def has_changed(
        available_field_value: AvailableFieldValue,
        changes: AvailableFieldValueInterface,
    ) -> bool:
        for key, value in changes.items():
            if getattr(available_field_value, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(available_field_value_id: int) -> int:
        available_field_value = AvailableFieldValue.query.filter(
            AvailableFieldValue.id == available_field_value_id
        ).first()
        if not available_field_value:
            raise AvailableFieldValueNotFoundException
        db.session.delete(available_field_value)
        db.session.commit()
        return available_field_value_id
