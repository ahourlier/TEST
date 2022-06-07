from app import db
import os
import copy
from datetime import datetime
from flask import g
from app.common.drive_utils import DriveUtils
from app.common.search import sort_query
from app.common.sheets_util import SheetsUtils
from app.common.tasks import create_task
from app.v2_imports.model import ImportType, ImportStatus, Imports
from app.v2_imports.error_handlers import (
    ImportNotFoundException,
    LogSheetNotCreatedException,
    ImportStillRunningException,
    WrongImportTypeException,
)
from app.v2_imports.interface import ImportInterface
from app.copro.copros.service import CoproService
from app.copro.syndic.service import SyndicService

IMPORT_DEFAULT_PAGE = 1
IMPORT_DEFAULT_PAGE_SIZE = 100
IMPORT_DEFAULT_SORT_FIELD = "id"
IMPORT_DEFAULT_SORT_DIRECTION = "asc"

IMPORT_TASK_QUEUE = "v2-import-queue"


class ImportsService:
    def get(import_id):
        current_import = Imports.query.get(import_id)
        if not current_import:
            raise ImportNotFoundException
        return current_import

    def list(
        page=IMPORT_DEFAULT_PAGE,
        size=IMPORT_DEFAULT_PAGE_SIZE,
        sort_by=IMPORT_DEFAULT_SORT_FIELD,
        direction=IMPORT_DEFAULT_SORT_DIRECTION,
        term=None,
        mission_id=None,
    ):
        q = sort_query(
            Imports.query,
            sort_by,
            direction,
        )

        if mission_id:
            q = q.filter(Imports.mission_id == mission_id)

        return q.paginate(page=page, per_page=size)

    def launch_import(payload: ImportInterface):
        payload["type"] = ImportType.SCAN.value
        payload["status"] = ImportStatus.RUNNING.value
        payload["author_id"] = g.user.id
        created_log_sheet = ImportsService.create_log_spreadsheet(payload)
        payload["log_sheet_id"] = created_log_sheet.get("id")
        new_import = Imports(**payload)
        db.session.add(new_import)
        db.session.commit()
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=IMPORT_TASK_QUEUE,
            uri=f"{os.getenv('API_URL')}/_internal/imports/run",
            method="PUT",
            payload={"import_id": new_import.id, "email": g.user.email},
        )
        return new_import

    def create_log_spreadsheet(created_import: ImportInterface):
        today = datetime.now().strftime("%Y-%m-%d")
        # todo create sheet only with service account
        created_sheet = SheetsUtils.create_sheet(
            payload={
                "properties": {
                    "title": f"Mission {created_import.get('mission_id')} - {created_import.get('name')} - {created_import.get('import_type')} - {today}"
                }
            },
            user_email=g.user.email,
        )
        if not created_sheet:
            raise LogSheetNotCreatedException
        return {"id": created_sheet.get("spreadsheetId")}

    def delete_import(current_import: Imports, import_id: int):

        if current_import.log_sheet_id:
            # todo create with service account as sheet will be created in shared drive with service account
            res = DriveUtils.delete_file(
                current_import.log_sheet_id, user_email=g.user.email
            )
            if not res:
                print(f"cannot delete log sheet for import {current_import.id}")

        db.session.delete(current_import)
        db.session.commit()

        return import_id

    def run_import(current_import: Imports):

        if current_import.status == ImportStatus.RUNNING.value:
            raise ImportStillRunningException

        if current_import.type != ImportType.SCAN.value:
            raise WrongImportTypeException

        current_import.status = ImportStatus.RUNNING.value
        current_import.type = ImportType.IMPORT.value
        db.session.commit()
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=IMPORT_TASK_QUEUE,
            uri=f"{os.getenv('API_URL')}/_internal/imports/run",
            method="PUT",
            payload={"import_id": current_import.id, "email": g.user.email},
        )
        return current_import

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
        running_import, logs, dry_run, user_email, A1_notation_filters
    ):
        """
        . Create a new tab either SCAN or IMPORT if dry run or not, with timestamp and add logs in
        . Remove default Sheet1 tab
        """
        now = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        if dry_run:
            created_tab = SheetsUtils.create_tab_on_existing_sheet(
                running_import.log_sheet_id, "SCAN-" + now, user_email
            )
            sheet_id = created_tab.get("spreadsheetId")
            SheetsUtils.add_values(
                sheet_id=sheet_id,
                range=f"{'SCAN-' + now}!{A1_notation_filters}",
                array_values=logs,
                user_email=user_email,
            )
            # Delete default Sheet1 tab after another tab exists
            resp = SheetsUtils.get_spreadsheet_by_datafilter(
                running_import.log_sheet_id, user_email=user_email
            )
            sheet_id_to_delete = resp.get("sheets")[0].get("properties").get("sheetId")
            SheetsUtils.delete_sheet(
                running_import.log_sheet_id, sheet_id_to_delete, user_email
            )
        else:
            created_tab = SheetsUtils.create_tab_on_existing_sheet(
                running_import.log_sheet_id, "IMPORT-" + now, user_email
            )
            SheetsUtils.add_values(
                sheet_id=created_tab.get("spreadsheetId"),
                range=f"{'IMPORT-'+ now}!{A1_notation_filters}",
                array_values=logs,
                user_email=user_email,
            )
