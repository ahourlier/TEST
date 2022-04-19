from app import db
import os
import copy
from datetime import datetime
from flask import g
from app.common.drive_utils import DriveUtils
from app.common.search import sort_query
from app.common.sheets_util import SheetsUtils
from app.common.tasks import create_task
from app.v2_exports.model import ExportStatus, Exports
from app.v2_exports.error_handlers import (
    ExportNotFoundException,
    LogSheetNotCreatedException,
)
from app.v2_exports.interface import ExportInterface

EXPORT_DEFAULT_PAGE = 1
EXPORT_DEFAULT_PAGE_SIZE = 100
EXPORT_DEFAULT_SORT_FIELD = "id"
EXPORT_DEFAULT_SORT_DIRECTION = "asc"

EXPORT_TASK_QUEUE = "v2-export-queue"


class ExportsService:
    def get(export_id):
        current_export = Exports.query.get(export_id)
        if not current_export:
            raise ExportNotFoundException
        return current_export

    def list(
        page=EXPORT_DEFAULT_PAGE,
        size=EXPORT_DEFAULT_PAGE_SIZE,
        sort_by=EXPORT_DEFAULT_SORT_FIELD,
        direction=EXPORT_DEFAULT_SORT_DIRECTION,
        term=None,
        mission_id=None,
    ):
        q = sort_query(
            Exports.query,
            sort_by,
            direction,
        )

        if mission_id:
            q = q.filter(Exports.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    def launch_export(payload: ExportInterface):
        payload["status"] = ExportStatus.RUNNING.value
        payload["author_id"] = g.user.id
        created_log_sheet = ExportsService.create_log_spreadsheet(payload)
        payload["export_sheet_id"] = created_log_sheet.get("id")
        new_export = Exports(**payload)
        db.session.add(new_export)
        db.session.commit()
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=EXPORT_TASK_QUEUE,
            uri=f"{os.getenv('API_URL')}/_internal/exports/run",
            method="PUT",
            payload={"export_id": new_export.id, "email": g.user.email},
        )
        return new_export

    def create_log_spreadsheet(created_export: ExportInterface):
        today = datetime.now().strftime("%Y-%m-%d")
        # todo create sheet only with service account
        created_sheet = SheetsUtils.create_sheet(
            payload={
                "properties": {
                    "title": f"Mission {created_export.get('mission_id')} - {created_export.get('name')} - {created_export.get('export_type')} - {today}"
                }
            },
            user_email=g.user.email,
        )
        if not created_sheet:
            raise LogSheetNotCreatedException
        return {"id": created_sheet.get("spreadsheetId")}

    def delete_export(current_export: Exports, export_id: int):

        if current_export.log_sheet_id:
            # todo create with service account as sheet will be created in shared drive with service account
            res = DriveUtils.delete_file(
                current_export.log_sheet_id, user_email=g.user.email
            )
            if not res:
                print(f"cannot delete log sheet for export {current_export.id}")

        db.session.delete(current_export)
        db.session.commit()

        return export_id

    def run_export(current_export: Exports):
        current_export.status = ExportStatus.RUNNING.value
        db.session.commit()
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=EXPORT_TASK_QUEUE,
            uri=f"{os.getenv('API_URL')}/_internal/exports/run",
            method="PUT",
            payload={"export_id": current_export.id, "email": g.user.email},
        )
        return current_export

    def format_address(row, indexes):
        """
        Create an address object to fit with db
        @param: row: array of values from spreadsheet
        @param: indexes: dict object with each attributes of address object and its position in spreadsheet
        should be in this format = {"number": 0, "street": 1, "postal_code": 2, "city": 3, "full_address": 4}
        @returns: address to format known by table Address in db
        """
        for key, value in indexes.items():
            if key == "full_address":
                indexes[
                    key
                ] = f"{indexes['number']} {indexes['street']}, {indexes['postal_code']} {indexes['city']}, France"
            else:
                indexes[key] = row[value]
        return indexes

    def insert_logs_in_tabs(
        running_export, logs, dry_run, user_email, A1_notation_filters
    ):
        """
        . Create a new tab EXPORT with timestamp and add logs in
        . Remove default Sheet1 tab
        """
        # TODO
        now = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        created_tab = SheetsUtils.create_tab_on_existing_sheet(
            running_export.log_sheet_id, "EXPORT-" + now, user_email
        )
        SheetsUtils.add_values(
            sheet_id=created_tab.get("spreadsheetId"),
            range=f"{'EXPORT-'+ now}!{A1_notation_filters}",
            array_values=logs,
            user_email=user_email,
        )
