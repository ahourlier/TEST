import copy

from app.copro.copros.service import CoproService
from app.v2_imports.service import ImportsService
from app.v2_imports.model import Imports


class CoproImport:
    def run_copro_import(
        running_import: Imports, dry_run, data, A1_notation_filters, user_email
    ):
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
            # Syndic has been specified in spreadsheet
            if row[5] is not None:
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
                CoproImport.process_copros(
                    json_data, running_import.mission_id, dry_run
                )
            )
        except Exception as e:
            print("An error occured while processing parsed copros")
            raise (e)
        ImportsService.insert_logs_in_tabs(
            running_import, logs, dry_run, user_email, A1_notation_filters
        )

    def process_copros(copro_objects, mission_id, dry_run):
        """Process import of list of copros"""
        logs = []
        # for each copro in import sheet
        for copro in copro_objects:
            # check if copro with same address in same mission exists and has not been deleted
            copro_exists = CoproService.search_by_address(
                copro.get("address_1"), mission_id
            )
            if copro_exists:
                # if exists, update
                logs.extend(
                    CoproImport.process_existing_copro(copro_exists, copro, dry_run)
                )
                continue
            # else create
            logs.extend(
                CoproImport.process_non_existing_copro(copro, mission_id, dry_run)
            )
        return logs

    def process_existing_copro(existing_copro, import_copro, dry_run):
        """Process a copro that already exists"""
        logs = []
        try:
            if not dry_run:
                # if importing and not scanning, update copro in db
                CoproService.update(
                    existing_copro, copy.deepcopy(import_copro), existing_copro.id
                )

            content = []
            content.append(
                [
                    "SUCCES",
                    "COPRO",
                    "UPDATE",
                    f"Adresse: {import_copro.get('address_1').get('full_address')}\nNom: {import_copro.get('name')}",
                    "",
                ]
            )
            if "syndic_name" in import_copro:
                content.append(
                    [
                        "SUCCES",
                        "SYNDIC",
                        "UPDATE",
                        f"Adresse: {import_copro.get('syndic_manager_address').get('full_address')}\nNom: {import_copro.get('syndic_name')}",
                        "",
                    ]
                )
            logs.extend(content)
        except Exception as e:
            # if an error occurred, add error log
            # TODO potential better error management for copro and syndic, more understandable error details
            content = []
            content.append(
                [
                    "ECHEC",
                    "COPRO",
                    "UPDATE",
                    f"Adresse: {import_copro.get('address_1').get('full_address')}\nNom: {import_copro.get('name')}",
                    f"{e}",
                ]
            )
            if "syndic_name" in import_copro:
                content.append(
                    [
                        "ECHEC",
                        "SYNDIC",
                        "UPDATE",
                        f"Adresse: {import_copro.get('syndic_manager_address').get('full_address')}\nNom: {import_copro.get('syndic_name')}",
                        f"{e}",
                    ]
                )
            logs.extend(content)
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

            content = []
            content.append(
                [
                    "SUCCES",
                    "COPRO",
                    "CREATION",
                    f"Adresse: {copro_object.get('address_1').get('full_address')}\nNom: {copro_object.get('name')}",
                    "",
                ]
            )
            if "syndic_name" in copro_object:
                content.append(
                    [
                        "SUCCES",
                        "SYNDIC",
                        "CREATION",
                        f"Adresse: {copro_object.get('syndic_manager_address').get('full_address')}\nNom: {copro_object.get('syndic_name')}",
                        "",
                    ]
                )
            logs.extend(content)

        except Exception as e:
            # if an error occurred, add error log
            content = []
            content.append(
                [
                    "ECHEC",
                    "COPRO",
                    "CREATION",
                    f"Adresse: {copro_object.get('address_1').get('full_address')}\nNom: {copro_object.get('name')}",
                    f"{e}",
                ]
            )
            if "syndic_name" in copro_object:
                content.append(
                    [
                        "ECHEC",
                        "SYNDIC",
                        "CREATION",
                        f"Adresse: {copro_object.get('syndic_manager_address').get('full_address')}\nNom: {copro_object.get('syndic_name')}",
                        f"{e}",
                    ]
                )
            logs.extend(content)
        return logs
