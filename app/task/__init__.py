from flask_restx import Namespace

from .model import Task

BASE_ROUTE = "task"

api = Namespace("Task", description="Task namespace")


def register_routes(api, app, root="api"):
    from .controller import api as task_api

    api.add_namespace(task_api, path=f"/{root}/{BASE_ROUTE}")
