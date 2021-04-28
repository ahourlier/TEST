from typing import List

from app import db
from app.project.disorders.error_handlers import disorder_type_not_found
import app.project.projects.service as projects_service
from app.project.work_types.exceptions import WorkTypeNotFoundException
from app.project.work_types.interface import WorkTypeInterface
from app.project.work_types.model import WorkType


class WorkTypeService:
    @staticmethod
    def create(new_attrs: WorkType) -> WorkType:
        projects_service.ProjectService.get_by_id(new_attrs.get("project_id"))

        work_type = WorkType(**new_attrs)
        db.session.add(work_type)
        db.session.commit()
        return work_type

    @staticmethod
    def create_list(
        work_types_values: List[WorkTypeInterface], project_id: int,
    ) -> List[WorkType]:

        work_types = []
        # Create corresponding work types
        for work_type in work_types_values:
            work_type["project_id"] = project_id
            work_types.append(WorkTypeService.create(work_type))

        return work_types

    @staticmethod
    def update_list(work_types_fields, project_id):
        # Delete
        old_work_types = WorkType.query.filter(WorkType.project_id == project_id).all()
        for old_work_type in old_work_types:
            WorkTypeService.delete_by_id(old_work_type.id)

        work_types = []
        # Re-create
        for wt in work_types_fields:
            wt["project_id"] = project_id
            work_types.append(WorkTypeService.create(wt))

        return work_types

    @staticmethod
    def delete_by_id(work_type_id: int) -> int or None:
        work_type = WorkType.query.filter(WorkType.id == work_type_id).first()
        if not work_type:
            raise WorkTypeNotFoundException
        db.session.delete(work_type)
        db.session.commit()
        return work_type_id
