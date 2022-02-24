from sqlalchemy import or_
from flask import g
from datetime import date

from app import db
from app.common.exceptions import EnumException
from app.common.firestore_utils import FirestoreUtils
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.task import Task, TaskType
from app.task.error_handlers import (
    TaskNotFoundException,
    BadFormatAssigneeException,
    EnumException as TaskEnumException,
    InvalidTaskTypeException,
    StepOrVersionMissingException,
)
from app.task.interface import TaskInterface
from app.thematique.exceptions import VersionNotFoundException, StepNotFoundException

TASK_DEFAULT_PAGE = 1
TASK_DEFAULT_PAGE_SIZE = 100
TASK_DEFAULT_SORT_FIELD = "reminder_date"
TASK_DEFAULT_SORT_DIRECTION = "asc"

ENUM_MAPPING = {
    "status": {"enum_key": "TaskStatus"},
}


class TaskService:
    @staticmethod
    def get(task_id: int, task_type: str = None) -> Task:
        task_query = Task.query.filter(Task.id == task_id)
        if task_type:
            task_query = task_query.filter(Task.task_type == task_type)
        
        task = task_query.first()
        if not task or task.is_deleted:
            raise TaskNotFoundException
        return task

    @staticmethod
    def create(new_attrs: TaskInterface):

        try:
            ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)
        except EnumException as e:
            raise TaskEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        TaskService.task_type_is_valid(new_attrs.get("task_type"))

        TaskService.check_task_payload_valid(new_attrs)

        firestore_service = FirestoreUtils()
        document = firestore_service.get_version_by_id(
            version_id=new_attrs.get("version_id")
        )
        if document.exists is None:
            raise VersionNotFoundException

        document = firestore_service.get_step_by_id(
            version_id=new_attrs.get("version_id"),
            step_id=new_attrs.get("step_id"),
        )
        if document.exists is None:
            raise StepNotFoundException

        new_task = Task(**new_attrs)
        new_task.author_id = g.user.id
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def get_all(
        page=TASK_DEFAULT_PAGE,
        size=TASK_DEFAULT_PAGE_SIZE,
        term=None,
        sort_by=TASK_DEFAULT_SORT_FIELD,
        direction=TASK_DEFAULT_SORT_DIRECTION,
        mission_id=None,
        assignee=None,
        step=None,
        version=None,
        task_type=None,
    ):
        q = sort_query(
            Task.query.filter(or_(Task.is_deleted == False, Task.is_deleted == None)),
            sort_by,
            direction,
        )
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term),
                )
            )

        if task_type and TaskService.task_type_is_valid(task_type):
            q = q.filter(Task.task_type == task_type)

        if mission_id:
            q = q.filter(Task.mission_id == mission_id)

        if assignee:
            try:
                assignee = [int(a) for a in assignee.split(",") if len(a)]
            except ValueError:
                raise BadFormatAssigneeException
            q = q.filter(Task.assignee_id.in_(assignee))

        if step:
            step = step.split(",")
            q = q.filter(Task.step_id.in_(step))

        if version:
            version = version.split(",")
            q = q.filter(Task.version_id.in_(version))

        count = q.count()
        tasks = q.all()
        # order by most close reminder date, past reminders at the end
        expired_tasks = []
        now = date.today()
        # moved expired tasks to the side
        # TODO ask Urbanis: status ? what to do with finished tasks ?
        for t in tasks:
            if t.reminder_date and t.reminder_date < now:
                expired_tasks.insert(0, t)
        # get their ids
        expired_ids = [t.id for t in expired_tasks]
        # remove them from the list
        tasks = [t for t in tasks if t.id not in expired_ids]
        # add them at the end
        tasks.extend(expired_tasks)
        # manually paginate
        tasks = tasks[(page - 1) * size : (page * size)]
        response = {"items": tasks, "page": page, "per_page": size, "total": count}

        return response

    @staticmethod
    def update(db_task: Task, changes: TaskInterface):

        try:
            ServicesUtils.check_enums(changes, ENUM_MAPPING)
        except EnumException as e:
            raise TaskEnumException(
                details=e.details,
                message=e.message,
                value=e.details.get("value"),
                allowed_values=e.details.get("allowed_values"),
                enum=e.details.get("enum"),
            )

        TaskService.task_type_is_valid(changes.get("task_type"))

        changes["step_id"] = db_task.step_id
        changes["version_id"] = db_task.version_id

        TaskService.check_task_payload_valid(changes)

        for forbidden_key in ["version_id", "step_id", "id", "author", "author_id"]:
            if forbidden_key in changes:
                del changes[forbidden_key]
        db_task.update(changes)
        db.session.commit()
        return db_task

    @staticmethod
    def delete(task_id: int):
        db_task = TaskService.get(task_id)
        db_task.soft_delete()
        db.session.commit()
        return task_id

    @staticmethod
    def task_type_is_valid(value):
        if value in [v.value for v in TaskType]:
            return True
        raise InvalidTaskTypeException

    @staticmethod
    def check_task_payload_valid(payload):
        if payload.get("task_type") == TaskType.TASK.value and (
            payload.get("version_id") is None or payload.get("step_id") is None
        ):
            raise StepOrVersionMissingException
        return True
