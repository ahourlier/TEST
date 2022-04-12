import copy
import traceback

from app import db

from app.copro.copros.service import CoproService
from app.building.service import BuildingService
from app.lot.service import LotService
from app.person.service import PersonService
from app.cle_repartition.service import CleRepartitionService
from app.cle_repartition.error_handlers import CleRepartitionNotFoundException
from app.person.schema import PersonSchema
from app.building.error_handlers import BuildingNotFoundException

from app.copro.copros.error_handlers import CoproNotFoundException
from app.person.error_handlers import PersonNotFoundException
from app.v2_imports.service import ImportsService
from app.v2_imports.model import Imports


class LotImport:
    def run_lot_import(
        running_import: Imports, dry_run, data, A1_notation_filters, user_email
    ):
        # init address fields' position in a row for copro
        address_copro_indexes = {
            "number": 1,
            "additional_info": 2,
            "street": 3,
            "postal_code": 4,
            "city": 5,
            "full_address": "",
        }
        # init address fields' position in a row for co_owner
        address_co_owner_indexes = {
            "number": 12,
            "additional_info": 13,
            "street": 14,
            "postal_code": 15,
            "city": 16,
            "full_address": "",
        }

        json_data = []
        for idx, row in enumerate(data):
            if idx == 0:
                # if headers, skip
                continue
            # init copro dict
            current_lot = {
                "building_name": row[0],
                "copro_address": ImportsService.format_address(
                    row, copy.deepcopy(address_copro_indexes)
                ),
                "lot_number": row[6],
                "client_number": row[7],
                "civility": row[8],
                "co_owner_last_name": row[9],
                "co_owner_first_name": row[10],
                "company_name": row[11],
                "co_owner_address": ImportsService.format_address(
                    row, copy.deepcopy(address_co_owner_indexes)
                ),
                "occupant_status": row[17],
                "cles_repartition": row[18],
            }

            json_data.append(current_lot)

        # init logs with headers
        logs = [["Statut", "Entité", "Action", "Détails", "Si erreurs, détails"]]
        try:
            # process copros and add logs to array
            content = LotImport.process_lots(
                json_data, running_import.mission_id, dry_run, user_email
            )
            logs.extend(content)
        except Exception as e:
            print("An error occured while processing parsed lots")
            print(traceback.format_exc())
            raise (e)
        finally:
            try:
                ImportsService.insert_logs_in_tabs(
                    running_import, logs, dry_run, user_email, A1_notation_filters
                )
                # Ensure import error status
                if len(logs) == 0:
                    raise Exception
                for i in range(len(logs)):
                    if logs[i][0] == "ECHEC":
                        raise Exception
            except Exception as e:
                print("An error occured while inserting logs in tabs")
                print(traceback.format_exc())
                raise (e)

    def process_lots(lot_objects, mission_id, dry_run, user_email):
        """Process import of list of copros"""
        # for each lot in import sheet
        logs = []
        for lot in lot_objects:
            try:
                # Search for unique copro from its address
                associated_copro = CoproService.search_by_address(
                    lot.get("copro_address"), mission_id
                )
                del lot["copro_address"]
                if not associated_copro:
                    raise CoproNotFoundException

            except Exception as e:
                print(traceback.format_exc())
                logs = []
                logs.extend(
                    [
                        [
                            "ECHEC",
                            "LOT",
                            "Can't define action before getting copro",
                            f"",
                            f"{traceback.format_exc()}",
                        ]
                    ]
                )
                return logs

            # Check existence of current lot to import
            lot_exists = LotService.search_by_unique_lot_number_in_copro(
                lot.get("lot_number"), associated_copro
            )
            if not lot_exists:
                logs.extend(
                    LotImport.process_new_lot(
                        lot, associated_copro, dry_run, user_email
                    )
                )
            else:
                logs.extend(
                    LotImport.process_existing_lot(
                        lot_exists, lot, associated_copro, dry_run, user_email
                    )
                )
        return logs

    def process_new_lot(lot_object, copro, dry_run, user_email):
        # Infos for logs
        building_created = False
        person_created = False
        try:
            # Manage building
            building = BuildingService.get_building_from_unique_name(
                lot_object.get("building_name"), copro
            )
            if not building:
                building_obj = {
                    "name": lot_object.get("building_name"),
                    "copro_id": copro.id,
                }
                building_created = True
                if not dry_run:
                    building = BuildingService.create(building_obj)

            building_name = lot_object.get("building_name")  # Keep for dry run logs
            del lot_object["building_name"]

            # Manage co-owner
            lastname = lot_object.get("co_owner_last_name")
            firstname = lot_object.get("co_owner_first_name")
            company_name = lot_object.get("company_name")
            civility = lot_object.get("civility")
            associated_person = PersonService.search_person_by_address_and_name(
                lot_object.get("co_owner_address"), lastname, firstname
            )
            if not associated_person:
                person_object = {}
                # Build object to create
                person_object["last_name"] = lastname
                person_object["civility"] = civility
                if firstname is not None:
                    person_object["first_name"] = firstname
                if company_name is not None:
                    person_object["company_name"] = company_name
                    person_object["is_physical_person"] = False
                else:
                    person_object["is_physical_person"] = True

                person_object["address"] = lot_object.get("co_owner_address")
                person_created = True
                # Create person if not exists
                if not dry_run:
                    associated_person = PersonService.create(person_object, user_email)

            # Keep for dry run logs
            person_log = {
                "last_name": lot_object["co_owner_last_name"],
                "first_name": lot_object["co_owner_first_name"],
                "address": lot_object["co_owner_address"],
                "civility": lot_object["civility"],
            }
            del lot_object["co_owner_last_name"]
            del lot_object["co_owner_first_name"]
            del lot_object["co_owner_address"]
            del lot_object["civility"]
            del lot_object["company_name"]

            # Manage cle_repartition
            lot_object = LotImport.get_cle_repartition_links(lot_object, copro)
            if not dry_run:
                # Manage Lot
                lot_object["copro_id"] = copro.id
                lot_object["building_id"] = building.id
                lot_object["owners"] = [PersonSchema().dump(associated_person)]
                LotService.create(copy.deepcopy(lot_object))

            content = LotImport.build_log_content(
                "CREATION",
                copro,
                building_name,
                lot_object,
                person_log,
                building_created,
                person_created,
            )
            logs = []
            logs.extend(content)

        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            logs = []
            logs.extend(
                [
                    [
                        "ECHEC",
                        "LOT",
                        "CREATION",
                        f"",
                        f"{traceback.format_exc()}",
                    ]
                ]
            )
        finally:
            return logs

    def process_existing_lot(existing_lot, import_lot, copro, dry_run, user_email):
        try:
            # Manage building
            building = BuildingService.get_building_from_unique_name(
                existing_lot.building.name, copro
            )
            if not building:
                # Building should exists
                raise BuildingNotFoundException
            building_obj = {"name": import_lot.get("building_name")}
            if not dry_run:
                building = BuildingService.update(building, building_obj)
            building_name = import_lot.get("building_name")  # Keep for dry run logs
            del import_lot["building_name"]

            # Manage co-owner
            person_object = {}
            lastname = import_lot.get("co_owner_last_name")
            firstname = import_lot.get("co_owner_first_name")
            company_name = import_lot.get("company_name")
            associated_person = PersonService.search_person_by_name_and_is_owner_in_lot(
                existing_lot, lastname, firstname, company_name
            )
            civility = import_lot.get("civility")
            person_object["last_name"] = lastname
            person_object["civility"] = civility
            if firstname is not None:
                person_object["first_name"] = firstname
            if company_name is not None:
                person_object["company_name"] = company_name
                person_object["is_physical_person"] = False
            else:
                person_object["is_physical_person"] = True
            person_object["address"] = import_lot.get("co_owner_address")

            if not dry_run:
                if not associated_person:
                    PersonService.remove_owners_from_lot(existing_lot)
                    # Replace all previous owners with a new one from import sheet
                    associated_person = PersonService.create(person_object, user_email)
                else:
                    # Update person if exists and is owner of current lot
                    associated_person = PersonService.update(
                        associated_person, person_object
                    )

            # Keep for dry run logs
            person_log = {
                "last_name": import_lot["co_owner_last_name"],
                "first_name": import_lot["co_owner_first_name"],
                "address": import_lot["co_owner_address"],
                "civility": import_lot["civility"],
            }
            del import_lot["co_owner_last_name"]
            del import_lot["co_owner_first_name"]
            del import_lot["co_owner_address"]
            del import_lot["civility"]
            del import_lot["company_name"]

            # Manage cle_repartition
            import_lot = LotImport.get_cle_repartition_links(import_lot, copro)
            if not dry_run:
                # Manage Lot
                import_lot["copro_id"] = copro.id
                import_lot["building_id"] = building.id
                import_lot["owners"] = [PersonSchema().dump(associated_person)]
                LotService.update(existing_lot, copy.deepcopy(import_lot))

            content = LotImport.build_log_content(
                "UPDATE", copro, building_name, import_lot, person_log
            )
            logs = []
            logs.extend(content)

        except Exception as e:
            db.session.rollback()
            print(traceback.format_exc())
            logs = []
            logs.extend(
                [
                    [
                        "ECHEC",
                        "LOT",
                        "CREATION",
                        f"",
                        f"{traceback.format_exc()}",
                    ]
                ]
            )
        finally:
            return logs

    def get_cle_repartition_links(lot_object, copro):
        links = []
        items = lot_object["cles_repartition"].split(";")
        for cle in items:
            label = cle.split("=")[0]
            tantieme = cle.split("=")[1]

            found_key = CleRepartitionService.get(label, copro.id)
            if found_key is None:
                print(
                    f"Cle Repartition with label {label} in copro {copro.id} not found.."
                )
                raise CleRepartitionNotFoundException
            # Get cle_repartition associated to label in current copro
            links.append({"cle_repartition_id": found_key.id, "tantieme": tantieme})
        lot_object["cles_repartition"] = links
        return lot_object

    def build_log_content(
        type,
        copro,
        building_name,
        lot_object,
        person_log,
        building_created=None,
        person_created=None,
    ):

        if type == "CREATION":

            current_logs = [
                f"Lot n°{lot_object.get('lot_number')}",
                f"Copro: '{copro.name}' found",
            ]
            if building_created:
                current_logs.append(f"Building - '{building_name}' created")
            else:
                current_logs.append(f"Building - '{building_name}' found")
            if person_created:
                current_logs.append(
                    f"Owner - {person_log['civility']} {person_log['last_name']}  with address '{person_log['address']['full_address']}' created"
                )
            else:
                current_logs.append(
                    f"Owner - {person_log['civility']} {person_log['last_name']}  with address '{person_log['address']['full_address']}' found"
                )
            current_logs.append(
                f"Specified repartition key have been found and associated to lot n°{lot_object.get('lot_number')}"
            )
            return [
                [
                    "SUCCES",
                    "LOT",
                    "CREATION",
                    "\n".join(current_logs),
                    "",
                ]
            ]
        else:
            current_logs = [
                f"Lot n°{lot_object.get('lot_number')}",
                f"Copro: '{copro.name}' found",
            ]
            current_logs.append(f"Building - '{building_name}' updated")
            current_logs.append(
                f"Owner - {person_log['civility']} {person_log['last_name']}  with address '{person_log['address']['full_address']}' updated"
            )
            current_logs.append(
                f"Specified repartition key have been updated on lot n°{lot_object.get('lot_number')}"
            )
            return [
                [
                    "SUCCES",
                    "LOT",
                    "UPDATE",
                    "\n".join(current_logs),
                    "",
                ]
            ]
