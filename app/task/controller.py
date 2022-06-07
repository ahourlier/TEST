from flask_accepts import accepts, responds
from flask import request, Response, jsonify, g
from flask_allows import requires
from flask_sqlalchemy import Pagination
from .model import TaskType

from . import task_api as api, event_api, Task
from .schema import TaskSchema, TaskPaginatedSchema, TaskUpdateSchema
from .service import (
    TaskService,
    TASK_DEFAULT_PAGE,
    TASK_DEFAULT_PAGE_SIZE,
    TASK_DEFAULT_SORT_FIELD,
    TASK_DEFAULT_SORT_DIRECTION,
)
from ..common.api import AuthenticatedApi
from ..common.permissions import has_mission_permission
from ..common.permissions import has_task_permission

SEARCH_PARAMS = [
    dict(name="page", type=int),
    dict(name="size", type=int),
    dict(name="term", type=str),
    dict(name="sortBy", type=str),
    dict(name="sortDirection", type=str),
    dict(name="missionId", type=int),
    dict(name="assignee", type=str),
    dict(name="step", type=str),
    dict(name="version", type=str),
    dict(name="taskType", type=str),
]


def get_task_type_from_url(path):
    if "task" in path:
        return TaskType.TASK.value
    if "event" in path:
        return TaskType.EVENT.value
    return None


# A Task is linked to a thematic, an event is only linked to a mission (tab called "Conduite de mission")
# They both have the exact same fields and expected behaviour


@api.route("")
@event_api.route("")
class TaskResource(AuthenticatedApi):
    """Task"""

    @accepts(*SEARCH_PARAMS, api=api)
    @responds(schema=TaskPaginatedSchema())
    def get(self) -> Pagination:
        """Get all tasks"""
        return TaskService.get_all(
            page=int(request.args.get("page", TASK_DEFAULT_PAGE)),
            size=int(request.args.get("size", TASK_DEFAULT_PAGE_SIZE)),
            term=request.args.get("term"),
            sort_by=request.args.get("sortBy", TASK_DEFAULT_SORT_FIELD),
            direction=request.args.get("sortDirection", TASK_DEFAULT_SORT_DIRECTION),
            mission_id=request.args.get("missionId")
            if request.args.get("missionId") not in [None, ""]
            else None,
            assignee=request.args.get("assignee")
            if request.args.get("assignee") not in [None, ""]
            else None,
            author=request.args.get("author")
            if request.args.get("author") not in [None, ""]
            else None,
            step=request.args.get("step")
            if request.args.get("step") not in [None, ""]
            else None,
            version=request.args.get("version")
            if request.args.get("version") not in [None, ""]
            else None,
            task_type=get_task_type_from_url(request.path),
            merge=request.args.get("merge"),
            user=g.user,
        )

    @accepts(schema=TaskSchema, api=api)
    @responds(schema=TaskSchema)
    @requires(has_mission_permission)
    def post(self) -> Task:
        """Create a task"""
        request.parsed_obj["task_type"] = get_task_type_from_url(request.path)
        return TaskService.create(request.parsed_obj)


@api.route("/<int:task_id>")
@api.param("TaskId", "Task unique id")
@event_api.route("/<int:task_id>")
@event_api.param("eventId", "Event unique id")
class TaskIdResource(AuthenticatedApi):
    """Task id resource"""

    @responds(schema=TaskSchema())
    def get(self, task_id: int):
        """Get one task"""
        task_type = get_task_type_from_url(request.path)
        return TaskService.get(task_id, task_type)

    @accepts(schema=TaskUpdateSchema, api=api)
    @responds(schema=TaskSchema)
    @requires(has_task_permission)
    def put(self, task_id: int) -> Task:
        """Update a task"""
        request.parsed_obj["task_type"] = get_task_type_from_url(request.path)
        db_task = TaskService.get(task_id, request.parsed_obj["task_type"])
        return TaskService.update(db_task, request.parsed_obj)

    @requires(has_task_permission)
    def delete(self, task_id: int) -> Response:
        """Delete a task"""
        task_type = get_task_type_from_url(request.path)
        id = TaskService.delete(task_id, task_type)
        return jsonify(dict(status="Success", id=id))
