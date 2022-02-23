from flask_restx import Namespace

from .model import Task, TaskType

task_api = Namespace("Task", description="Task namespace")
event_api = Namespace("Task", description="Task namespace")


def register_routes(api, app, root="api"):
    from .controller import api as task_api
    from .controller import event_api

    api.add_namespace(task_api, path=f"/{root}/task")
    api.add_namespace(event_api, path=f"/{root}/event")
