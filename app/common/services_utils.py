import copy
import logging
from typing import List

from app.common.exceptions import EnumException
from app.referential.enums.service import AppEnumService


class ServicesUtils:
    @staticmethod
    def clean_attrs(attrs: dict, excluded_fields: []):
        """Remove excluded fields from entring attrs and return them"""

        extracted_fields = {}

        for field in excluded_fields:
            if field in attrs:
                extracted_fields[field] = attrs[field]
                del attrs[field]

        return extracted_fields

    @staticmethod
    def fetch_dict_fields_from_object(
        base_entity,
        base_fields_to_remove=["id", "updated_at", "created_at"],
        extra_fields_to_remove=[],
    ):
        """From a given db entity, returns all fields (no sql alchemy relations),
        minus the provided base_fields_to_remove and extra_fields_to_remove"""
        fields_dict = base_entity.__dict__.copy()
        # Remove all child/nested and relationship values
        for key in list(fields_dict):
            if key not in base_entity.__table__.columns.keys():
                del fields_dict[key]
        fields_to_remove = base_fields_to_remove.copy()
        fields_to_remove.extend(extra_fields_to_remove)
        # Remove provided fields :
        for field in fields_to_remove:
            del fields_dict[field]
        return fields_dict.copy()

    @staticmethod
    def set_nested_dict(dic, keys, value, append=False):
        """Small util to set value into nested dict.
        Can append new value into existing as dict or list"""
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        if append and keys[-1] in dic:
            items_list = dic[keys[-1]]
            if isinstance(items_list, list) and isinstance(value, list):
                items_list.append(value)
            elif isinstance(items_list, dict) and isinstance(value, dict):
                items_list = {**items_list, **value}
            else:
                logging.error("Append value canceled")
                return
            dic[keys[-1]] = items_list
        else:
            dic[keys[-1]] = value

    @staticmethod
    def deep_copy_list_of_dicts(list):
        """Returns a deepcopy of the given list of dicts"""
        copy_list = []
        for li in list:
            copy_item = copy.deepcopy(li)
            copy_list.append(copy_item)
        return copy_list

    @staticmethod
    def check_enums(payload, key_mapping):
        enum_list = list(map(lambda x: key_mapping[x]["enum_key"], key_mapping))
        enums = AppEnumService.get_enums(enum_list)
        for key in key_mapping:
            if payload.get(key) is not None and payload.get(key) not in enums.get(
                key_mapping[key]["enum_key"], []
            ):
                exception = EnumException(
                    enum=key_mapping[key]["enum_key"],
                    value=payload.get(key),
                    allowed_values=", ".join(
                        enums.get(key_mapping[key]["enum_key"], [])
                    ),
                    details={
                        "enum": key_mapping[key]["enum_key"],
                        "value": payload.get(key),
                        "allowed_values": ", ".join(
                            enums.get(key_mapping[key]["enum_key"], [])
                        ),
                    },
                )
                raise exception
        return
