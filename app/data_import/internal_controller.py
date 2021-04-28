from flask import request
import app.data_import.service as data_import_service
from app.internal_api.base import InternalAPIView


class OpenImportTask(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        data_import_service.DataImportService.open_import(
            data.get("sheet_id"), data.get("user_email"), data.get("mission_id")
        )
        return "OK"


class RegisterNewEntity(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        data_import_service.DataImportService.next_data_import_iteration(
            import_id=data.get("import_id"),
            sheet_id=data.get("sheet_id"),
            row_id=data.get("row_id"),
            entities_keys_map=data.get("entities_keys_map"),
            mission_id=data.get("mission_id"),
        )
        return "OK"


class ActivateImportedProjects(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        data_import_service.DataImportService.activate_imported_projects(
            projects_id_list=data.get("projects_id_list"),
        )
        return "OK"


class CloseImport(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        data_import_service.DataImportService.close_import(
            import_id=data.get("import_id"),
        )
        return "OK"


class RollbackDeteleProjects(InternalAPIView):
    def post(self):
        data = request.get_json(force=True)
        data_import_service.DataImportService.delete_canceled_projects(
            projects_id_list=data.get("projects_id_list"),
        )
        return "OK"
