from sqlalchemy import or_
from flask import g
from app import db
from app.common.firestore_utils import FirestoreUtils
from app.common.search import sort_query
from app.common.services_utils import ServicesUtils
from app.task import Task
from app.task.exceptions import TaskNotFoundException
from app.task.interface import TaskInterface
from app.thematique.exceptions import VersionNotFoundException, StepNotFoundException

TASK_DEFAULT_PAGE = 1
TASK_DEFAULT_PAGE_SIZE = 100
TASK_DEFAULT_SORT_FIELD = "id"
TASK_DEFAULT_SORT_DIRECTION = "desc"

ENUM_MAPPING = {
    "status": {"enum_key": "TaskStatus"},
}


class TaskService:
    @staticmethod
    def get(task_id: int) -> Task:
        task = Task.query.get(task_id)
        if not task or task.is_deleted:
            raise TaskNotFoundException
        return task

    @staticmethod
    def create(new_attrs: TaskInterface):

        ServicesUtils.check_enums(new_attrs, ENUM_MAPPING)

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
    ):
        q = sort_query(
            Task.query.filter(or_(Task.is_deleted == False, Task.is_deleted == None)),
            sort_by,
            direction,
        )
        if term is not None:
            search_term = f"%{term}%"
            q = q.filter(
                or_(Task.title.ilike(search_term), Task.description.ilike(search_term),)
            )

        if mission_id:
            q = q.filter(Task.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    @staticmethod
    def update(db_task: Task, changes: TaskInterface):
        for forbidden_key in ['version_id', 'step_id', 'id', 'author', 'author_id']:
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
