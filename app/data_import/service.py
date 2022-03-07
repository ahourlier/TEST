import json
import logging
import os
from typing import List

from flask import request, g
from flask_restx import abort

from app import db
from app.common.data_import_utils import (
    SPREADSHEET_STRUCTURE,
    DataImportUtils,
    SheetsList,
    SheetFieldsTypes,
    INSTANTIATION_ORDER,
    BaseEntities,
)
from app.common.exceptions import InconsistentUpdateIdException
from app.common.tasks import create_task
from app.data_import.model import DataImport
from app.data_import.error_handlers import DataImportNotFoundException
from app.data_import.interface import DataImportInterface
from app.data_import.model import DataImportStatus
from app.mission.missions import Mission
from app.project.projects.service import PROJECT_INIT_QUEUE_NAME

import app.project.projects.service as projects_service

IMPORT_PROJECTS_QUEUE_NAME = "import-projects-queue"
REGISTER_ENTITY_QUEUE_NAME = "register-entity-queue"
ACTIVATE_PROJECTS_QUEUE_NAME = "active-projects-queue"
CLOSE_IMPORT_QUEUE_NAME = "close-import-queue"
DELETE_PROJECT_QUEUE_NAME = "delete-project-queue"


class DataImportService:
    @staticmethod
    def get_by_id(data_import_id: str) -> DataImport:
        db_data_import = DataImport.query.get(data_import_id)
        if db_data_import is None:
            raise DataImportNotFoundException
        return db_data_import

    @staticmethod
    def create(new_attrs: DataImportInterface) -> DataImport:
        """Create a new data_import"""
        data_import = DataImport(**new_attrs)
        db.session.add(data_import)
        db.session.commit()
        return data_import

    @staticmethod
    def update(
        data_import: DataImport,
        changes: DataImportInterface,
        force_update: bool = False,
    ) -> DataImport:
        if force_update or DataImportService.has_changed(data_import, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != data_import.id:
                raise InconsistentUpdateIdException()
            data_import.update(changes)
            db.session.commit()
        return data_import

    @staticmethod
    def has_changed(data_import: DataImport, changes: DataImportInterface) -> bool:
        for key, value in changes.items():
            if getattr(data_import, key) != value:
                return True
        return False

    @staticmethod
    def import_projects(mission: Mission, data_sheet_id: str):
        """Launch tasks to begin multiple projects import"""
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=IMPORT_PROJECTS_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/data_import/projects",
            method="POST",
            payload={
                "mission_id": mission.id,
                "sheet_id": data_sheet_id,
                "user_email": g.user.email,
            },
        )

        return "Success"

    # V2 SPREADSHEET_STRUCTURE should be given as parameters
    # V2 Deal with mission_id in a more generic way
    @staticmethod
    def open_import(sheet_id, user_email, mission_id):
        """From a given data sheet, import multiple projects and sub_entities"""

        # With given SPREADSHEET_STRUCTURE, we reconstruct Google's "A1notations" fields ready
        # to be injected into the API
        labels_A1_locations = [
            f"{sheet_name}!{sheet_dict['labels_position']}"
            for (sheet_name, sheet_dict) in SPREADSHEET_STRUCTURE.items()
        ]
        data_A1_locations = [
            f"{sheet_name}!{sheet_dict['data_position']}"
            for (sheet_name, sheet_dict) in SPREADSHEET_STRUCTURE.items()
        ]
        # Two object are fetched from given spreadsheet :
        # labels of the sheets, and the data itself
        labels = DataImportUtils.fetch_data_from_sheet(
            sheet_id, user_email, labels_A1_locations
        )
        data = DataImportUtils.fetch_data_from_sheet(
            sheet_id, user_email, data_A1_locations
        )
        new_import_object_fields = {
            "status": DataImportStatus.ON_GOING.value,
            "user_email": user_email,
            "data": json.dumps(data),
            "labels": json.dumps(labels),
        }
        db_data_import = DataImportService.create(new_import_object_fields)

        entities_keys_map = {
            value.get("model"): {} for key, value in SPREADSHEET_STRUCTURE.items()
        }

        # Launch the first entity creation, with the first row data from the first sheet
        # Recursively, the "launch_new_registration" will call himself until
        # all row from all sheets are imported
        DataImportService.next_data_import_registration(
            db_data_import.id, 0, 0, entities_keys_map, mission_id
        )
        return "Success"

    @staticmethod
    def close_import(import_id: int):
        """End import worflow. Make raw data empty, update import status and commit changes"""
        db_data_import = DataImportService.get_by_id(import_id)
        changes = {"status": DataImportStatus.DONE.value, "data": None, "labels": None}
        DataImportService.update(db_data_import, changes)
        db.session.commit()
        logging.info("Import succeedded")
        return "Success"

    @staticmethod
    def next_data_import_iteration(
        import_id: int,
        sheet_id: int,
        row_id: int,
        entities_keys_map: int,
        mission_id: int,
    ):
        """For given sheet and row id (corresponding to a sheet data loaded into base),
        create one entity and launch a task for the next index of the data"""

        db_data_import = DataImportService.get_by_id(import_id)
        sheet_name = INSTANTIATION_ORDER.get(sheet_id)

        # Recursion end. Import workflow must be closed.
        if not sheet_name:
            created_projects_id = DataImportService.extract_projects_id(
                entities_keys_map
            )
            DataImportService.initialize_projects_drives_task(created_projects_id)
            DataImportService.activate_imported_projects(created_projects_id, import_id)
            return "End import"

        sheet_data = json.loads(db_data_import.data).get(sheet_name)

        # Import workflow keeps going within the next sheet
        if row_id > len(sheet_data) - 1:
            return DataImportService.next_data_import_registration(
                import_id, sheet_id + 1, 0, entities_keys_map, mission_id
            )

        label_fields_map = SPREADSHEET_STRUCTURE.get(sheet_name).get(
            "labels_fields_map"
        )

        if sheet_name == SheetsList.PROJECTS.value:
            date_status_fields_map = SPREADSHEET_STRUCTURE.get(sheet_name).get(
                "date_status_fields_map"
            )
            label_fields_map = DataImportService.add_date_status_to_label_fields(
                sheet_data[row_id],
                json.loads(db_data_import.labels).get(sheet_name)[0],
                label_fields_map,
                date_status_fields_map,
            )
        # Fetch new entity fields/values correspondances
        new_entity_fields = DataImportService.build_entity_labels_fields_list(
            row_fields=sheet_data[row_id],
            labels_fields_map=label_fields_map,
            labels_lists=json.loads(db_data_import.labels).get(sheet_name)[0],
        )

        # To be removed in v2. Not enough generic
        # Insert specific projects values
        if sheet_name == SheetsList.PROJECTS.value:
            projects_labels_fields_map = label_fields_map
            new_entity_fields[
                "identifiant de la mission associée"
            ] = projects_labels_fields_map.get("identifiant de la mission associée")
            new_entity_fields["identifiant de la mission associée"][
                "value"
            ] = mission_id
            new_entity_fields["actif"] = projects_labels_fields_map.get("actif")
            new_entity_fields["actif"]["value"] = "NON"

        # A new entity is registered into database
        if new_entity_fields:
            entities_keys_map = DataImportService.instantiate_new_entity(
                sheet_name=sheet_name,
                new_entity_fields=new_entity_fields,
                entities_keys_map=entities_keys_map,
                mission_id=mission_id,
            )

        # Import workflow keeps going with the next row registration
        return DataImportService.next_data_import_registration(
            import_id, sheet_id, row_id + 1, entities_keys_map, mission_id
        )

    @staticmethod
    def instantiate_new_entity(
        sheet_name, new_entity_fields, entities_keys_map, mission_id
    ):
        """
        With SPREADSHEET_STRUCTURE infos and data from a sheet row, build and register a
        new db entity
        """
        model_name = SPREADSHEET_STRUCTURE.get(sheet_name).get("model")
        (
            new_attrs,
            primary_key_field,
            phone_numbers,
            disorder_types,
            work_types,
        ) = DataImportService.build_new_entity_attrs(
            sheet_name, model_name, entities_keys_map, new_entity_fields, mission_id
        )
        new_entity = DataImportService.insert_new_entity(
            model_name, new_attrs, entities_keys_map, primary_key_field.get("value")
        )
        # Register phone_numbers (special workflow)
        if phone_numbers:
            DataImportService.register_phone_numbers(
                phone_numbers, new_entity.id, entities_keys_map
            )
        if disorder_types:
            DataImportService.register_disorder_types(
                disorder_types, new_entity.id, entities_keys_map
            )
        if work_types:
            DataImportService.register_work_types(
                work_types, new_entity.id, entities_keys_map
            )
        # Update entities_keys_map with new entity database primary key
        entities_keys_map[model_name][primary_key_field.get("value")] = getattr(
            new_entity, primary_key_field.get("field")
        )
        return entities_keys_map

    def add_date_status_to_label_fields(
        fields_values, fields_label, labels_fields_map, date_status_fields_map
    ):
        imported_status_name = None
        for index, label in enumerate(fields_label):
            if label == "status":
                imported_status_name = fields_values[index]
                break

        if imported_status_name:
            for status_name in date_status_fields_map:
                if status_name == imported_status_name:
                    found_db_field_name = date_status_fields_map[status_name]
                    labels_fields_map["date du status"] = {}
                    labels_fields_map["date du status"]["field"] = found_db_field_name
                    labels_fields_map["date du status"][
                        "type"
                    ] = SheetFieldsTypes.DATE_DAY.value
                    labels_fields_map["date du status"][
                        "model"
                    ] = BaseEntities.PROJECT.value
                    break
        return labels_fields_map

    # V2 : phone_number could be refactored as "generic extra fields"
    @staticmethod
    def build_new_entity_attrs(
        sheet_name, model_name, entities_keys_map, new_entity_fields, mission_id
    ):
        """From the new_entity_fields list, return :
        1 : a new_attr dict ready to be injected to instantiate a new SQL ALchemy Object
        2 : a primary_key_field object containing infos and value of the primary field
        """
        new_attrs = {}
        phone_numbers = []
        disorder_types = []
        work_types = []

        for field_name, field_infos in new_entity_fields.items():
            if not field_infos.get("value"):
                continue
            if field_infos.get("type") == SheetFieldsTypes.PRIMARY_ID.value:
                # Store primary keys for future relational mapping
                primary_key_field = DataImportService.validate_primary_key(
                    sheet_name,
                    field_infos,
                    entities_keys_map,
                    model_name,
                )
                continue
            elif field_infos.get("type") == SheetFieldsTypes.FOREIGN_ID.value:
                # Replace fields identified as "foreign by" by real db foreign keys
                value = DataImportService.fetch_foreign_key(
                    field_infos, entities_keys_map, sheet_name
                )
            elif field_infos.get("type") == SheetFieldsTypes.PHONE.value:
                phone_numbers.append(DataImportUtils.extract_phone_attrs(field_infos))
                continue
            elif field_infos.get("type") == SheetFieldsTypes.USER_EMAIL.value:
                value = DataImportUtils.fetch_user_id(mission_id, field_infos)
                if not isinstance(value, int):
                    DataImportService.rollback_import(
                        entities_keys_map,
                        sheet=sheet_name,
                        value=primary_key_field.get("value"),
                        field=field_name,
                        message=value,
                    )
            elif field_infos.get("type") == SheetFieldsTypes.DISORDER_TYPE.value:
                disorder_types.extend(
                    DataImportUtils.extract_disorder_types_attrs(field_infos)
                )
                continue
            elif field_infos.get("type") == SheetFieldsTypes.WORK_TYPE.value:
                work_types.extend(DataImportUtils.extract_work_types_attrs(field_infos))
                continue
            else:
                value = DataImportService.fetch_formatted_value(
                    sheet_name,
                    field_infos,
                    primary_key_field,
                    field_name,
                    entities_keys_map,
                )
            new_attrs[field_infos.get("field")] = value

        return new_attrs, primary_key_field, phone_numbers, disorder_types, work_types

    @staticmethod
    def validate_primary_key(sheet_name, field_infos, entities_keys_map, model_name):
        """Check primary key information. If valid, returns it. Else, cancel import workflow"""
        primary_key_field = None
        primary_key_already_registered = (
            field_infos.get("value") in entities_keys_map[model_name]
        )
        if (
            not field_infos.get("value")
            or not field_infos.get("value")
            or primary_key_already_registered
        ):

            DataImportService.rollback_import(
                entities_keys_map,
                sheet_name,
                message="Incorrect or absent entity ID",
            )
        if primary_key_field:
            DataImportService.rollback_import(
                entities_keys_map,
                sheet_name,
                message=f"A primary ID was already provided for the entity {primary_key_field.get('value')}.",
            )
        return field_infos

    @staticmethod
    def fetch_foreign_key(field_infos, entities_keys_map, sheet_name):
        """Within the entities_keys_map, fetch the real database foreign key corresponding.
        Cancel import if none can be found"""
        try:
            model = field_infos.get("foreign_model")
            return entities_keys_map.get(model).get(field_infos.get("value"))
        except Exception as e:
            DataImportService.rollback_import(
                entities_keys_map,
                sheet=sheet_name,
                entity=field_infos.get("model"),
                field=field_infos.get("field"),
                value=field_infos.get("value"),
                message=f"No matching foreign key found",
                error=e,
            )

    @staticmethod
    def fetch_formatted_value(
        sheet_name, field_infos, primary_key_field, field_name, entities_keys_map
    ):
        try:
            return DataImportUtils.format_value(
                field_infos.get("value"), field_infos.get("type")
            )
        except Exception as e:
            DataImportService.rollback_import(
                entities_keys_map,
                sheet_name,
                primary_key_field.get("value"),
                field_name,
                e,
            )

    @staticmethod
    def build_entity_labels_fields_list(
        row_fields,
        labels_fields_map,
        labels_lists,
    ):
        """For each element of a given sheet row, map the sheet value
        with field infos provided by the SPREADSHEET_STRUCTURE main object"""
        new_entity = {}
        for i, value in enumerate(row_fields):
            field_infos = labels_fields_map.get(labels_lists[i])
            if field_infos:
                field_infos["value"] = value
                new_label_field_map = {labels_lists[i]: field_infos}
                new_entity = {**new_entity, **new_label_field_map}
        return new_entity

    @staticmethod
    def insert_new_entity(
        model_name, new_attrs, entities_keys_map, primary_key_value=None
    ):
        """Insert a new entity in db, based on provided new_attrs"""
        model = DataImportUtils.fetch_model(model_name)
        new_entity = None
        try:
            new_entity = model(**new_attrs)
            db.session.add(new_entity)
            db.session.commit()
        except Exception as e:
            DataImportService.rollback_import(
                entities_keys_map,
                entity=model_name,
                value=primary_key_value,
                message="Impossible to insert entity into database",
                error=e,
            )
        return new_entity

    @staticmethod
    def activate_imported_projects(projects_id_list: List, import_id):
        """Loop over provided projects_ids and activate them when import is over"""
        for project_id in projects_id_list:
            db.session.query(DataImportUtils.fetch_model("Project")).filter_by(
                id=project_id
            ).update({"active": True})
        db.session.commit()
        DataImportService.close_import_task(import_id)

    @staticmethod
    def register_phone_numbers(phone_numbers_attrs, parent_id, entities_keys_map):
        """
        Phone numbers are treated apart (because it should have been painful
        for users to enter phones in a dedicated sheet, like others entities are.
        Instead, phones numbers are considered as "fields", so we need to extract them,
        then register them
        """
        for attr in phone_numbers_attrs:
            attr["resource_id"] = parent_id
            DataImportService.insert_new_entity(
                BaseEntities.PHONE_NUMBER.value, attr, entities_keys_map
            )

    @staticmethod
    def register_disorder_types(disorder_type_attrs, parent_id, entities_keys_map):
        """
        Disorder types are treated apart (because it should have been painful
        for users to enter disorder types in a dedicated sheet, like others entities are.
        """
        for attr in disorder_type_attrs:
            attr["disorder_id"] = parent_id
            DataImportService.insert_new_entity(
                BaseEntities.DISORDER_TYPE.value, attr, entities_keys_map
            )

    @staticmethod
    def register_work_types(work_type_attrs, project_id, entities_keys_map):
        """
        Work types are treated apart (because it should have been painful
        for users to enter work types in a dedicated sheet, like others entities are.
        """
        for attr in work_type_attrs:
            attr["project_id"] = project_id
            DataImportService.insert_new_entity(
                BaseEntities.WORK_TYPE.value, attr, entities_keys_map
            )

    @staticmethod
    def next_data_import_registration(
        import_id: int,
        sheet_id: int,
        row_id: int,
        entities_keys_map: int,
        mission_id: int,
    ):
        """Launch task to register a new entity"""
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=REGISTER_ENTITY_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/data_import/register",
            method="POST",
            payload={
                "mission_id": mission_id,
                "sheet_id": sheet_id,
                "row_id": row_id,
                "entities_keys_map": entities_keys_map,
                "import_id": import_id,
            },
        )

        return "Success"

    @staticmethod
    def rollback_import(
        entities_keys_map,
        sheet=None,
        entity=None,
        field=None,
        value=None,
        message="Incorrect data provided",
        error=None,
    ):
        """Cancel and rollback import. Log an error message then remove recursively all priory created projects"""
        message = f"IMPORT CANCELED. {message}. Sheet_name : {sheet}. Entity ID : {entity}. Field : {field}. Value : {value} Error details : {error}"
        logging.error(message)
        logging.info("Rollback launched")
        canceled_projects_id = DataImportService.extract_projects_id(entities_keys_map)
        DataImportService.delete_canceled_project_task(canceled_projects_id)
        abort(400)

    @staticmethod
    def delete_canceled_projects(projects_id_list):
        if len(projects_id_list) > 0:
            logging.info(f"deletion canceled project ID {projects_id_list[0]}")
            projects_service.ProjectService.hard_delete_by_id(projects_id_list[0])
            projects_id_list.pop(0)
            DataImportService.delete_canceled_project_task(projects_id_list)
        else:
            logging.info("Rollback successfully deleted all canceled projects")

    @staticmethod
    def activate_projects_task(projects_id_list):
        """Launch task to activate imported projects"""
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=ACTIVATE_PROJECTS_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/data_import/activate",
            method="POST",
            payload={
                "projects_id_list": projects_id_list,
            },
        )

        return "Success"

    @staticmethod
    def close_import_task(import_id):
        """Launch task to close import"""
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=CLOSE_IMPORT_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/data_import/close",
            method="POST",
            payload={
                "import_id": import_id,
            },
        )

        return "Success"

    @staticmethod
    def initialize_projects_drives_task(projects_id_list: List):
        """Loop over provided projects_ids and launch tasks to initialize
        all projects drive folders tree"""
        for project_id in projects_id_list:
            create_task(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("QUEUES_LOCATION"),
                queue=PROJECT_INIT_QUEUE_NAME,
                uri=f"{os.getenv('API_URL')}/_internal/projects/init-drive",
                method="POST",
                payload={
                    "project_id": project_id,
                },
            )

    @staticmethod
    def delete_canceled_project_task(projects_id_list: List):
        """Launch task to delete the next item of the provided list"""
        create_task(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("QUEUES_LOCATION"),
            queue=DELETE_PROJECT_QUEUE_NAME,
            uri=f"{os.getenv('API_URL')}/_internal/data_import/rollback",
            method="POST",
            payload={
                "projects_id_list": projects_id_list,
            },
        )

    @staticmethod
    def extract_projects_id(entities_keys_map):
        return [
            project_db_id
            for project_sheet_id, project_db_id in entities_keys_map.get(
                BaseEntities.PROJECT.value
            ).items()
        ]
