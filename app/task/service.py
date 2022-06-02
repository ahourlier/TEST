from sqlalchemy import String, cast, or_
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
        q = Task.query.filter(Task.id == task_id)
        if task_type:
            q = q.filter(Task.task_type == task_type)
        task = q.first()
        if not task or task.is_deleted:
            raise TaskNotFoundException
        return task

    @staticmethod
    def get_by_entity(entity_id, entity_key) -> Task:
        q = Task.query.filter(entity_id == cast(Task.path[entity_key], String))
        return q.all()

    def get_by_thematique_version_id(version_id) -> Task:
        q = Task.query.filter(version_id == Task.version_id)
        return q.all()

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
        author=None,
        assignee=None,
        step=None,
        version=None,
        task_type=None,
        merge=None,
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
        # Merge overrides task type: get both types
        if merge is not None and merge == "true":
            pass
        elif task_type and TaskService.task_type_is_valid(task_type):
            q = q.filter(Task.task_type == task_type)

        if mission_id:
            q = q.filter(Task.mission_id == mission_id)

        if assignee:
            try:
                assignee = [int(a) for a in assignee.split(",") if len(a)]
            except ValueError:
                raise BadFormatAssigneeException
            q = q.filter(Task.assignee_id.in_(assignee))

        if author:
            try:
                author = [int(a) for a in author.split(",") if len(a)]
            except ValueError:
                raise BadFormatAssigneeException
            q = q.filter(Task.author_id.in_(author))

        if step:
            step = step.split(",")
            q = q.filter(Task.step_id.in_(step))

        if version:
            version = version.split(",")
            q = q.filter(Task.version_id.in_(version))

        count = q.count()
        tasks = q.all()

        if sort_by == "custom":
            tasks = TaskService.custom_tasks_sort(tasks)

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
    def delete(task_id: int, task_type: str):
        db_task = TaskService.get(task_id, task_type)
        db_task.soft_delete()
        db.session.commit()
        return task_id

    @staticmethod
    def delete_from_entity_id(entity_id, entity_key):
        tasks = TaskService.get_by_entity(str(entity_id), entity_key)
        for task in tasks:
            task.soft_delete()

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

    @staticmethod
    def custom_tasks_sort(tasks):
        """
        - tasks with expired reminder_date in status "In progress" or "To do"
        - tasks closest to unexpired_date reminder in "In progress" or "To do" status
        - tasks without date_reminder in "In progress" or "To do" status
        - tasks without date_reminder with "Completed" status
        - tasks with reminder_date in "Completed" status
        """
        expired_tasks_active = []
        future_tasks_active = []
        no_remind_task_active = []
        no_remind_tasks_inactive = []
        remind_tasks_inactive = []

        now = date.today()
        for t in tasks:
            if t.reminder_date:
                if t.status == "Terminée" or t.status == "Non concernée":
                    remind_tasks_inactive.insert(0, t)

                if t.reminder_date < now:
                    if t.status == "A faire" or t.status == "En cours":
                        expired_tasks_active.insert(0, t)

                if t.reminder_date >= now:
                    if t.status == "A faire" or t.status == "En cours":
                        future_tasks_active.insert(0, t)

            else:
                if t.status == "A faire" or t.status == "En cours":
                    no_remind_task_active.insert(0, t)
                if t.status == "Terminée" or t.status == "Non concernée":
                    no_remind_tasks_inactive.insert(0, t)

        expired_tasks_active = sorted(
            expired_tasks_active, key=lambda t: t.reminder_date
        )
        future_tasks_active = sorted(future_tasks_active, key=lambda t: t.reminder_date)
        remind_tasks_inactive = sorted(
            remind_tasks_inactive, key=lambda t: t.reminder_date
        )

        tasks = expired_tasks_active
        tasks.extend(future_tasks_active)
        tasks.extend(no_remind_task_active)
        tasks.extend(no_remind_tasks_inactive)
        tasks.extend(remind_tasks_inactive)

        return tasks
