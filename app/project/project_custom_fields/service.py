from operator import or_
from typing import List
import logging

from flask_sqlalchemy import Pagination

from app import db
from app.common.exceptions import (
    InconsistentUpdateIdException,
    InvalidSearchFieldException,
)
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.mission.custom_fields import CustomField
from app.mission.custom_fields.model import FieldsCategories
from app.project.project_custom_fields import CustomFieldValue
from app.project.project_custom_fields.exceptions import (
    ProjectCustomFieldNotFoundException,
    CustomFieldValueNotFoundException,
)
from app.project.project_custom_fields.interface import (
    ProjectCustomFieldInterface,
    CustomFieldValueInterface,
)
from app.project.project_custom_fields.model import ProjectCustomField
import app.project.projects.service as projects_service

PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE = 1
PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE_SIZE = 100
PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_FIELD = "id"
PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION = "desc"


class ProjectCustomFieldService:
    @staticmethod
    def get_all(
        page=PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE,
        size=PROJECT_CUSTOM_FIELDS_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_FIELD,
        direction=PROJECT_CUSTOM_FIELDS_DEFAULT_SORT_DIRECTION,
        project_id=None,
        category=None,
    ) -> Pagination:
        q = sort_query(ProjectCustomField.query, sort_by, direction)
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(or_(ProjectCustomField.value.ilike(search_term),))

        if project_id is not None:
            q = q.filter(ProjectCustomField.project_id == project_id)

        # Filter by category
        if category is not None and category not in FieldsCategories.__members__:
            raise InvalidSearchFieldException()
        if category is not None:
            q = q.filter(
                ProjectCustomField.custom_field.has(
                    CustomField.category == FieldsCategories[category].value
                )
            )

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def get_by_id(project_custom_field_id: str) -> ProjectCustomField:
        db_project_custom_field = ProjectCustomField.query.get(project_custom_field_id)
        if db_project_custom_field is None:
            raise ProjectCustomFieldNotFoundException
        return db_project_custom_field

    @staticmethod
    def create(
        new_attrs: ProjectCustomFieldInterface, project_id=None
    ) -> ProjectCustomField:
        """Create a new project_custom_field associated to a project"""
        if project_id is not None:
            new_attrs["project_id"] = project_id
        projects_service.ProjectService.get_by_id(new_attrs.get("project_id"))

        extracted_fields = ServicesUtils.clean_attrs(new_attrs, ["multiple_values"])
        project_custom_field = ProjectCustomField(**new_attrs)
        db.session.add(project_custom_field)
        db.session.commit()

        # Create multiple_values associated to the project_custom_field
        if "multiple_values" in extracted_fields:
            CustomFieldValueService.create_update_list(
                project_custom_field.id, extracted_fields["multiple_values"]
            )

        return project_custom_field

    @staticmethod
    def update(
        project_custom_field: ProjectCustomField,
        changes: ProjectCustomFieldInterface,
        force_update: bool = False,
    ) -> ProjectCustomField:
        extracted_fields = ServicesUtils.clean_attrs(
            changes, ["project_id", "multiple_values"]
        )
        if force_update or ProjectCustomFieldService.has_changed(
            project_custom_field, changes
        ):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != project_custom_field.id:
                raise InconsistentUpdateIdException()
            project_custom_field.update(changes)
            db.session.commit()

        # Update multiple_values associated to the project_custom_field
        if "multiple_values" in extracted_fields:
            CustomFieldValueService.create_update_list(
                project_custom_field.id, extracted_fields["multiple_values"]
            )

        return project_custom_field

    @staticmethod
    def create_update_list(project_id, changes: List, category: str):
        project = projects_service.ProjectService.get_by_id(project_id)
        original_project_custom_fields_id = [
            custom_field.id
            for custom_field in project.custom_fields
            if category == custom_field.custom_field.category
        ]

        changes_cf_id = [
            custom_field_value["id"]
            for custom_field_value in changes
            if "id" in custom_field_value
        ]

        for custom_field_value in changes:
            # Create
            if "id" not in custom_field_value:
                ProjectCustomFieldService.create(custom_field_value.copy(), project_id)
            # Update
            else:
                custom_field = ProjectCustomFieldService.get_by_id(
                    custom_field_value["id"]
                )
                ProjectCustomFieldService.update(
                    custom_field, custom_field_value.copy()
                )

        # Delete obsolete project_custom_fields
        for original_id in original_project_custom_fields_id:
            if original_id not in changes_cf_id:
                ProjectCustomFieldService.delete_by_id(original_id)

        return project.custom_fields

    @staticmethod
    def has_changed(
        project_custom_field: ProjectCustomField, changes: ProjectCustomFieldInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(project_custom_field, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(project_custom_field_id: int) -> int:
        project_custom_field = ProjectCustomField.query.filter(
            ProjectCustomField.id == project_custom_field_id
        ).first()
        if not project_custom_field:
            raise ProjectCustomFieldNotFoundException
        db.session.delete(project_custom_field)
        db.session.commit()
        return project_custom_field_id


class CustomFieldValueService:
    @staticmethod
    def get_by_id(custom_field_value_id: str) -> CustomFieldValue:
        db_custom_field_value = CustomFieldValue.query.get(custom_field_value_id)
        if db_custom_field_value is None:
            raise CustomFieldValueNotFoundException
        return db_custom_field_value

    @staticmethod
    def create(
        new_attrs: CustomFieldValueInterface, project_custom_field_id: None
    ) -> CustomFieldValue:
        """Create a new custom_field_value associated to a project_custom_field"""
        if project_custom_field_id is not None:
            new_attrs["project_custom_field_id"] = project_custom_field_id
        ProjectCustomFieldService.get_by_id(new_attrs.get("project_custom_field_id"))

        custom_field_value = CustomFieldValue(**new_attrs)
        db.session.add(custom_field_value)
        db.session.commit()
        return custom_field_value

    @staticmethod
    def update(
        custom_field_value: CustomFieldValue,
        changes: CustomFieldValueInterface,
        force_update: bool = False,
    ) -> CustomFieldValue:
        ServicesUtils.clean_attrs(changes, ["project_custom_field_id"])
        if force_update or CustomFieldValueService.has_changed(
            custom_field_value, changes
        ):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != custom_field_value.id:
                raise InconsistentUpdateIdException()
            custom_field_value.update(changes)
            db.session.commit()
        return custom_field_value

    @staticmethod
    def create_update_list(project_custom_field_id, changes: List):
        project_custom_field = ProjectCustomFieldService.get_by_id(
            project_custom_field_id
        )

        CustomFieldValueService.delete_all_for_project_custom_field_id(
            project_custom_field_id, True
        )
        if changes:
            for field_value in changes:
                CustomFieldValueService.create(
                    field_value.copy(), project_custom_field_id
                )

        return project_custom_field.multiple_values

    @staticmethod
    def has_changed(
        custom_field_value: CustomFieldValue, changes: CustomFieldValueInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(custom_field_value, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(custom_field_value_id: int) -> int:
        custom_field_value = CustomFieldValue.query.filter(
            CustomFieldValue.id == custom_field_value_id
        ).first()
        if not custom_field_value:
            raise CustomFieldValueNotFoundException
        db.session.delete(custom_field_value)
        db.session.commit()
        return custom_field_value_id

    @staticmethod
    def delete_all_for_project_custom_field_id(
        project_custom_field_id: int, commit: bool = False
    ):
        CustomFieldValue.query.filter(
            CustomFieldValue.project_custom_field_id == project_custom_field_id
        ).delete()
        if commit:
            db.session.commit()
