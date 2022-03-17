from .model import DataImport
from flask_restx import Namespace

data_import_api = Namespace("Data_Import", description="Data Import namespace")
from .internal_controller import (
    OpenImportTask,
    RegisterNewEntity,
    ActivateImportedProjects,
    CloseImport,
    RollbackDeteleProjects,
)

BASE_ROUTE = "data_upload"


def register_routes(api, app, root="api"):
    from app.data_import.controller import data_import_api

    api.add_namespace(data_import_api, path=f"/{root}/{BASE_ROUTE}")


def register_internal_routes(bp):
    prefix = "/data_import"

    bp.add_url_rule(
        f"{prefix}/register",
        view_func=RegisterNewEntity.as_view("register"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/projects",
        view_func=OpenImportTask.as_view("import-projects"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/activate",
        view_func=ActivateImportedProjects.as_view("activate"),
        methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/close", view_func=CloseImport.as_view("close"), methods=["POST"],
    )

    bp.add_url_rule(
        f"{prefix}/rollback",
        view_func=RollbackDeteleProjects.as_view("rollback"),
        methods=["POST"],
    )
