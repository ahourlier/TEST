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
        q = sort_query(Imports.query, sort_by, direction,)

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
        return {
            "id": created_sheet.get("spreadsheetId"),
        }

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

    def run_copro_import(running_import: Imports, dry_run, data, user_email):
        """
        Import copro from data in spreadsheet
        @param: running_import: db object of running import
        @param: dry_run: boolean if we need to create/update objects in db or not
        @param: data: data from spreadsheet with this format
        [
            [header1, header2, ....]
            [data1, data2, ....]
        ]
        """
        # init address fields' position in a row for copro
        address_copro_indexes = {
            "number": 0,
            "street": 1,
            "postal_code": 2,
            "city": 3,
            "full_address": "",
        }
        # init address fields' position in a row for syndic
        address_syndic_indexes = {
            "number": 6,
            "street": 7,
            "postal_code": 8,
            "city": 9,
            "full_address": "",
        }

        json_data = []
        for idx, row in enumerate(data):
            if idx == 0:
                # if headers, skip
                continue
            # init copro dict
            current_copro = {
                "name": row[4],
                "address_1": ImportsService.format_address(
                    row, copy.deepcopy(address_copro_indexes)
                ),
            }
            if row[5] not in ["", None]:
                # if has syndic, add info to copro
                current_copro["syndic_name"] = row[5]
                current_copro["syndic_manager_address"] = ImportsService.format_address(
                    row, copy.deepcopy(address_syndic_indexes)
                )

            json_data.append(current_copro)

        # init logs with headers
        logs = [["Statut", "Entité", "Action", "Détails", "Si erreurs, détails"]]
        try:
            # process copros and add logs to array
            logs.extend(
                ImportsService.process_copros(
                    json_data, running_import.mission_id, dry_run
                )
            )
        except Exception as e:
            print("An error occured while processing parsed copros")
            raise (e)
        # send logs to log sheet
        SheetsUtils.add_values(
            sheet_id=running_import.log_sheet_id,
            range="A:J",
            array_values=logs,
            user_email=user_email,
        )

    def process_copros(copro_objects, mission_id, dry_run):
        """Process import of list of copros"""
        logs = []
        # for each copro in import sheet
        for copro in copro_objects:
            # check if copro with same address in same mission exists
            copro_exists = CoproService.search_by_address(
                copro.get("address_1"), mission_id
            )
            if copro_exists:
                # if exists, update
                logs.extend(
                    ImportsService.process_existing_copro(copro_exists, copro, dry_run)
                )
                continue
            # else create
            logs.extend(
                ImportsService.process_non_existing_copro(copro, mission_id, dry_run)
            )
        return logs

    def process_existing_copro(existing_copro, import_copro, dry_run):
        """Process a copro that already exists"""
        print(import_copro)
        logs = []
        try:
            if not dry_run:
                # if importing and not scanning, update copro in db
                CoproService.update(
                    existing_copro, copy.deepcopy(import_copro), existing_copro.id
                )

            # add logs for copro and syndic update
            logs.extend(
                [
                    [
                        "SUCCES",
                        "COPRO",
                        "UPDATE",
                        f"Adresse: {import_copro.get('address_1').get('full_address')}\nNom: {import_copro.get('name')}",
                        "",
                    ],
                    [
                        "SUCCES",
                        "SYNDIC",
                        "UPDATE",
                        f"Adresse: {import_copro.get('syndic_manager_address').get('full_address')}\nNom: {import_copro.get('syndic_name')}",
                        "",
                    ],
                ]
            )
        except Exception as e:
            # if an error occurred, add error log
            # TODO potential better error management for copro and syndic, more understandable error details
            # TODO handle model change of syndic (migrated to copro model)
            logs.extend(
                [
                    [
                        "ECHEC",
                        "COPRO",
                        "UPDATE",
                        f"Adresse: {import_copro.get('address_1').get('full_address')}\nNom: {import_copro.get('name')}",
                        f"{e}",
                    ],
                    [
                        "ECHEC",
                        "SYNDIC",
                        "UPDATE",
                        f"Adresse: {import_copro.get('syndic_manager_address').get('full_address')}\nNom: {import_copro.get('syndic_name')}",
                        f"{e}",
                    ],
                ]
            )
        return logs

    def process_non_existing_copro(copro_object, mission_id, dry_run):
        """Process a copro that does not exist in db (to create)"""
        # add mission id
        copro_object["mission_id"] = mission_id
        logs = []
        try:
            if not dry_run:
                # if importing and not scanning, create copro in db
                CoproService.create(copy.deepcopy(copro_object))

            # add logs for copro and syndic creation
            logs.extend(
                [
                    [
                        "SUCCES",
                        "COPRO",
                        "CREATION",
                        f"Adresse: {copro_object.get('address_1').get('full_address')}\nNom: {copro_object.get('name')}",
                        "",
                    ],
                    [
                        "SUCCES",
                        "SYNDIC",
                        "CREATION",
                        f"Adresse: {copro_object.get('syndic_manager_address').get('full_address')}\nNom: {copro_object.get('syndic_name')}",
                        "",
                    ],
                ]
            )
        except Exception as e:
            # if an error occurred, add error log
            # TODO potential better error management for copro and syndic, more understandable error details
            # TODO handle model change of syndic (migrated to copro model)
            logs.extend(
                [
                    [
                        "ECHEC",
                        "COPRO",
                        "CREATION",
                        f"Adresse: {copro_object.get('address_1').get('full_address')}\nNom: {copro_object.get('name')}",
                        f"{e}",
                    ],
                    [
                        "ECHEC",
                        "SYNDIC",
                        "CREATION",
                        f"Adresse: {copro_object.get('syndic_manager_address').get('full_address')}\nNom: {copro_object.get('syndic_name')}",
                        f"{e}",
                    ],
                ]
            )
        return logs

    def run_lot_import(running_import: Imports, dry_run, data):
        print("Running lot import")
        print(f"Dry run? : {dry_run}")

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
