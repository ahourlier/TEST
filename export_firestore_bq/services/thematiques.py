from copy import deepcopy
import json
from typing import List
from config import (
    BQ_SCHEMA_ADDRESS,
    BQ_SCHEMA_FINANCEUR,
    BQ_SCHEMA_TEL,
    DEFAULT_FIELDS,
    FIELDS_MAPPING,
)
from services.bq import BQService
from services.firestore import FirestoreUtils
import unidecode


def process_template(template, firestore_utils: FirestoreUtils):
    """
    Prepare export for each versions coming from that template
    @params: template: DocumentSnapshot
    @params: firestore_utils: FirestoreUtils instance
    """
    # if (
    #     template.get("scope") != "copro"
    #     or template.get("thematique_name") != "SUIVI_FINANCEMENTS_PC_ET_PPIC"
    # ):
    #     return

    print(
        f"fetching all versions for thematique {template.get('thematique_name')} and scope {template.get('scope')}"
    )
    versions = firestore_utils.query_version(
        thematique_name=template.get("thematique_name"), scope=template.get("scope")
    )
    data = []
    bq_columns = deepcopy(DEFAULT_FIELDS)
    # for each versions, fetch steps and create model
    for version in versions:
        # fetch all steps for the version
        steps = firestore_utils.get_steps_by_version_id(version.id)
        # update bq schema for table and data
        bq_columns, steps_data = process_steps(steps, bq_columns)
        # prepare version details
        version_details = {
            "version_name": version.get("version_name"),
            "version_date": version.get("version_date"),
            "version_id": version.id,
            "thematique_name": template.get("thematique_name"),
            "resource_id": version.get("resource_id"),
        }
        # fill in version details
        steps_data = list(map(lambda step: {**step, **version_details}, steps_data))
        # update data
        data.extend(steps_data)
    # DEBUG create file with data
    with open('current_data.json', 'w') as f:
        json.dump(data, f)
    # instantiate BigQuery service
    bq_service = BQService()
    # create table
    table = bq_service.create_table(
        f"{template.get('scope')}_{template.get('thematique_name').lower()}", bq_columns
    )
    try:
        # try to load data
        bq_service.load_data_from_json(table, data, bq_columns)
        print(f"done with {table.table_id}")
    except Exception as e:
        # if not working, just logging to keep the script running
        print(f"FAILED TO LOAD TABLE FOR {table.table_id}")
        print(e)


def process_steps(steps: List, bq_columns: List[dict]):
    """
    Update model for bq table and format data to be sent in bq
    @params: steps: List of steps
    @params: bq_columns: Dict with columns for bq table
    """
    current_data = []
    for step in steps:
        step_dict = step.to_dict()
        # update bq model
        bq_columns, step_data = process_data_from_step(
            step_dict.get("fields"), bq_columns, {}
        )
        # filling step metadata
        step_metadata = {
            "step_status": step_dict.get("metadata").get("status"),
            "step_name": step_dict.get("metadata").get("name"),
            "step_id": step.id,
        }
        # add data to global array
        current_data.append({**step_data, **step_metadata})
    return bq_columns, current_data


def process_data_from_step(data: dict, bq_columns: List[dict], current_data):
    """
    Update model and format data for BQ table
    """
    # for each field and its settings
    for field_name, field_settings in data.items():
        # remove possible accents
        field_name = unidecode.unidecode(field_name)
        # check if field was already added
        idx = field_already_exists(field_name, bq_columns)
        if idx > -1:
            # first group is called default_group, needs to be processed
            if field_name == "default_group":
                # process default group
                for value in field_settings.get("value"):
                    (
                        bq_columns[idx]["fields"],
                        current_data[field_name],
                    ) = process_data_from_step(value, bq_columns[idx]["fields"], {})
                continue
        # create new field
        new_field = {
            "name": field_name,
            "type": FIELDS_MAPPING[field_settings.get("type")],
            "mode": "REPEATED" if field_settings.get("multiple") else "NULLABLE",
        }
        # if is type "group", process recursively
        if field_settings.get("type") == "group":
            # initiate fields for record
            new_field["fields"] = []
            # if group can be duplicated, handle as array of groups
            if field_settings.get("multiple"):
                current_data[field_name] = []
            for value in field_settings.get("value"):
                # process sub groups
                new_field["fields"], formatted_data = process_data_from_step(
                    value, new_field["fields"], {}
                )
                # if group can be duplicated, add to array
                if field_settings.get("multiple"):
                    current_data[field_name].append(formatted_data)
                else:
                    # else replace value
                    current_data[field_name] = formatted_data
        else:
            # remove all NULL values to avoid BQ errors
            field_settings["value"] = clear_all_none_values(field_settings.get("value"))
            # custom check for financeurs
            if "financeur" in field_name and "autocomplete" in field_settings.get("type"):
                # remove all financeurs that are not dict
                field_settings["value"] = (
                    [
                        financeur
                        for financeur in field_settings.get("value")
                        if type(financeur) == dict
                    ]
                )
                # remove funding scenarios because not to be exported
                for financeur in field_settings["value"]:
                    del financeur["funding_scenarios"]
            # if not group, check if is multiple, and has a value
            if field_settings.get("multiple"):
                current_data[field_name] = field_settings.get("value")
            elif len(field_settings.get("value")):
                current_data[field_name] = field_settings.get("value")[0]
            else:
                current_data[field_name] = (
                    [] if new_field.get("mode") == "REPEATED" else None
                )
        # specific test for phone, address, financeur fields because they have specific format
        if field_settings.get("type") in ["phone", "telephone"]:
            new_field["fields"] = deepcopy(BQ_SCHEMA_TEL)
        if field_settings.get("type") == "address":
            new_field["fields"] = deepcopy(BQ_SCHEMA_ADDRESS)
        if "financeur" in field_name and new_field.get("type") == "RECORD":
            new_field["fields"] = deepcopy(BQ_SCHEMA_FINANCEUR)
        # if field was never added to schema, add it
        if idx == -1:
            bq_columns.append(new_field)
    return bq_columns, current_data


def field_already_exists(field_name, bq_columns: List[dict]):
    """
    Check if field has already been added to model
    @params: field_name: Str field name
    @params: bq_columns: List of fields already added to the model
    """
    for idx, f in enumerate(bq_columns):
        if f.get("name") == unidecode.unidecode(field_name):
            return idx
    return -1


def clear_all_none_values(array):
    """
    BQ does not accept NULL values in arrays, so this method removes them
    @params: array: Array to clean
    """
    return [x for x in array if x]
