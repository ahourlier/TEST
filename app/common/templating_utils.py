import json
import re
from datetime import date, datetime
from enum import Enum
from typing import List
import logging

import pytz

import app.project.projects.service as projects_service
from app.common.constants import (
    FRENCH_DATE_FORMAT,
    DATE_MATCH_REGEX,
    DATE_FORMAT,
    FRENCH_DATE_AND_HOUR,
)
from app.mission.custom_fields import CustomField
from app.mission.monitors.model import MonitorField
from app.project.funders_monitoring_values import FunderMonitoringValue
from app.project.project_custom_fields.model import ProjectCustomField

REQUESTER_TITLES = {
    "mme": "Mme",
    "m": "M.",
    "mandmme": "M et Mme",
    "mmes": "Mmes",
    "messrs": "Messrs",
}


class ValuesTypes(Enum):
    VALID = "Valid"
    INVALID_PLACEHOLDER = "INVALID PLACEHOLDER"
    WRONG_INDEX = "WRONG INDEX"


class TemplatingUtils:
    @staticmethod
    def template_value(
        field_name, value, status: str = ValuesTypes.VALID.value, message: str = None
    ):
        """Return a formatted dict containing information about a field, his corresponding value, status.
        TemplatingUtils uses this to apply specific treatments for different situations :
        valid value, valid value non-readable, valid None value, or invalid/ non-existant field"""
        return {
            "field_name": field_name,
            "value": value,
            "status": status,
            "message": message,
        }

    @staticmethod
    def extract_placeholders(g_docs):
        """Extract placeholders identified by the syntax "{{...}}" in a google docs."""
        if type(g_docs) == "dict":
            doc_str = json.dumps(g_docs)
        if type(g_docs) == "str":
            doc_str = g_docs
        else:
            doc_str = str(g_docs)
        matches = re.findall("{{(.*?)}}", doc_str)
        return list(dict.fromkeys(matches))

    @staticmethod
    def get_changes_mapper(placeholders: List, project_id: int):
        """Return a changes_mapper dict such as each key is the original placeholder
        and each value is the corresponding data based on the provided project.
        Log invalid values/placeholders"""
        project = projects_service.ProjectService.get_by_id(project_id)

        changes_mapper = {}
        for tag in placeholders:
            value_response = TemplatingUtils.fetch_raw_value(tag, project)
            if value_response["status"] == ValuesTypes.VALID.value:
                formatted_value = TemplatingUtils.format_value(
                    value_response["value"], tag=tag
                )
                if formatted_value:
                    changes_mapper["{{" + tag + "}}"] = formatted_value
                else:
                    logging.error(
                        f"The value {value_response['value']} for placeholder {tag} cannot be formatted"
                    )
            elif value_response["status"] == ValuesTypes.WRONG_INDEX.value:
                changes_mapper["{{" + tag + "}}"] = " "
                logging.error(
                    f"{value_response.get('status')}. {value_response.get('message')}"
                )
            else:
                logging.error(
                    f"{value_response.get('status')}. {value_response.get('message')}"
                )
        return changes_mapper

    @staticmethod
    def format_value(raw_value, tag=None):
        """From a raw value, provides a readable, formatted version of the value"""
        readable_types = [str, int, float, date, datetime, bool]
        if type(raw_value) not in readable_types and raw_value is not None:
            return None
        if raw_value is None:
            # Null value in base must be formatted as empty values
            return " "

        if tag is not None:
            if tag == "requester.title":
                return str(REQUESTER_TITLES.get(raw_value))

        # Boolean conversion to french
        if type(raw_value) is bool:
            if raw_value:
                return "oui"
            else:
                return "non"
        # Date conversion to french
        if type(raw_value) is date:
            return raw_value.strftime(FRENCH_DATE_FORMAT)
        if type(raw_value) is datetime:
            local_tz = pytz.timezone("Europe/Paris")
            return (
                pytz.utc.localize(raw_value)
                .astimezone(local_tz)
                .strftime(FRENCH_DATE_AND_HOUR)
            )
        if type(raw_value) is str and re.match(DATE_MATCH_REGEX, raw_value):
            # Some dates are retrieved as strings, so we need a special treatment
            raw_value = datetime.strptime(raw_value, DATE_FORMAT)
            return raw_value.strftime(FRENCH_DATE_FORMAT)
        return str(raw_value)

    @staticmethod
    def fetch_raw_value(field: str, project):
        """Based on a string field chain such as "requester.last_name",
        return the corresponding value"""
        if field.startswith("$"):
            return TemplatingUtils.fetch_custom_field_value(field, project)
        elif field.startswith("&"):
            return TemplatingUtils.fetch_monitoring_field_value(field, project)
        else:
            return TemplatingUtils.fetch_standard_field_value(field, project)

    @staticmethod
    def fetch_custom_field_value(field: str, project):
        """Fetch value from a custom field placeholder identified as '$my_custom_field'
        If custom_field has multiple values, retrieves item of the list identified by his index : '$my_custom_field/index'"""
        field = field[1:]
        splitted_field = field.split("/")
        project_custom_field = (
            ProjectCustomField.query.filter(ProjectCustomField.project_id == project.id)
            .filter(
                ProjectCustomField.custom_field.has(
                    CustomField.name == splitted_field[0]
                )
            )
            .first()
        )
        if project_custom_field is None:
            return TemplatingUtils.template_value(
                splitted_field[0],
                None,
                status=ValuesTypes.INVALID_PLACEHOLDER.value,
                message=f"No custom field found with the placeholder {field}",
            )
        if len(splitted_field) == 2 and splitted_field[1].isdecimal():
            try:
                index = int(splitted_field[1]) - 1
                value = project_custom_field.multiple_values[index].value
                return TemplatingUtils.template_value(field, value)
            except:
                return TemplatingUtils.template_value(
                    splitted_field[0],
                    None,
                    status=ValuesTypes.WRONG_INDEX.value,
                    message=f"No custom field found with the field {splitted_field[0]}, at the index : {splitted_field[1]}",
                )
        return TemplatingUtils.template_value(field, project_custom_field.value)

    @staticmethod
    def fetch_monitoring_field_value(field: str, project):
        """Fetch value from a monitoring field placeholder identified as '&my_monitoring_field'
        If monitoring_field has multiple values (one for each funder associated to the project,
        retrieves item of the list identified by his index : '&my_monitoring_field/index'"""
        field = field[1:]
        splitted_field = field.split("/")
        funder_monitoring_values = (
            FunderMonitoringValue.query.filter(
                FunderMonitoringValue.project_id == project.id
            )
            .filter(
                FunderMonitoringValue.monitor_field.has(
                    MonitorField.name == splitted_field[0]
                )
            )
            .order_by(FunderMonitoringValue.funder_id)
            .all()
        )
        if len(funder_monitoring_values) == 0:
            return TemplatingUtils.template_value(
                splitted_field[0],
                None,
                status=ValuesTypes.INVALID_PLACEHOLDER.value,
                message=f"No monitoring field value found with the placeholder {field}",
            )
        if len(splitted_field) == 2 and splitted_field[1].isdecimal():
            try:
                index = int(splitted_field[1]) - 1
                value = funder_monitoring_values[index].value
                return TemplatingUtils.template_value(field, value)
            except:
                return TemplatingUtils.template_value(
                    splitted_field[0],
                    None,
                    status=ValuesTypes.WRONG_INDEX.value,
                    message=f"No monitoring value found with the field {splitted_field[0]}, at the index : {splitted_field[1]}",
                )
        return TemplatingUtils.template_value(field, funder_monitoring_values[0].value)

    @staticmethod
    def fetch_standard_field_value(field_chain: str, entity):
        """From a provided field chain such as "requester.last_name",
        search recursively into the base entity for the corresponding value"""
        splitted_field = field_chain.split(".")
        if entity is None:
            return TemplatingUtils.template_value(
                field_chain,
                None,
                status=ValuesTypes.INVALID_PLACEHOLDER.value,
                message=f"The field '{field_chain}' does not match any valid entity",
            )
        sub_entity_response = TemplatingUtils.fetch_sub_entity(
            splitted_field[0], entity
        )
        if (
            len(splitted_field) == 1
            or sub_entity_response["status"] != ValuesTypes.VALID.value
            or sub_entity_response["value"] is None
        ):
            return sub_entity_response
        else:
            del splitted_field[0]
            field = ".".join(splitted_field)
            return TemplatingUtils.fetch_standard_field_value(
                field, sub_entity_response.get("value")
            )

    @staticmethod
    def fetch_sub_entity(field: str, entity):
        """From a given entity, returns the sub_entity matching the provided field.
        If the field is a list, retrieves item identified by his index : 'field/index'"""
        if "/" in field:
            splitted_field = field.split("/")
            if len(splitted_field) == 2 and splitted_field[1].isdecimal():
                sub_entity = getattr(entity, splitted_field[0], None)
                try:
                    sub_entity.sort(key=lambda x: x.id)
                    value = sub_entity[int(splitted_field[1]) - 1]
                    return TemplatingUtils.template_value(field, value)
                except:
                    return TemplatingUtils.template_value(
                        splitted_field[0],
                        None,
                        status=ValuesTypes.WRONG_INDEX.value,
                        message=f"No item into list '{splitted_field[0]}' found with index : {splitted_field[1]}",
                    )
            return TemplatingUtils.template_value(
                splitted_field[0],
                None,
                status=ValuesTypes.INVALID_PLACEHOLDER.value,
                message=f"The subfield '{splitted_field[0]}' does not match any valid entity",
            )
        value = getattr(entity, field, "#ERROR_FIELD")
        if value != "#ERROR_FIELD":
            return TemplatingUtils.template_value(field, value)
        else:
            return TemplatingUtils.template_value(
                field,
                None,
                status=ValuesTypes.INVALID_PLACEHOLDER.value,
                message=f"The subfield '{field}' does not match any valid entity",
            )
