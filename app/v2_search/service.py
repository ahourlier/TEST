from datetime import datetime
import json

from sqlalchemy import inspect

from app.building.model import Building

from .config_structure import (
    ENTITY_TO_MODEL_MAPPING,
    ENTITY_TO_DEFAULT_MAPPING,
    MAPPER_ENTITY_TO_ORDER_DEFAULT_FIELDS,
    ENTITY_TO_ENUMS_MAPPING,
    MAPPING_TYPE_TO_UNKNOWN_COLUMN,
    ENTITY_TO_CONFIG_AUTOCOMPLETE,
)
from .config_sql_relations import (
    ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING,
    ENTITY_TO_COMPLEX_RELATION_MAPPING,
)

from .complex_filters import ComplexFilters
from ..referential.enums.service import AppEnumService
from app.common.search import SearchService

from app.combined_structure.model import CombinedStructure
from app.lot.model import Lot


class StructureService:
    def get_structure_from_entity(entity, structure):
        """
        Introspect model and return structure with column_name and column_type
        """
        if entity not in ENTITY_TO_MODEL_MAPPING:
            return f"Entity {entity} has no model reference... Choose either 'mission', 'lot', 'building', 'copro' or 'combined_structure'"

        model = ENTITY_TO_MODEL_MAPPING[entity]
        inst = inspect(model)
        for column in inst.c:
            structure.append(
                {"name": column.name, "type": str(column.type), "multiple": True}
            )

        return structure

    def add_label_fields(entity, structure):
        """
        Add i18n label to each field
        """
        for item in structure:
            item["label"] = f"search.{entity}.fields.{item['name']}"
        return structure

    def add_one_to_one_fields(entity, structure):
        """
        Add item to structure which are not existing columns in model
        and referenced in one to one relation mapper
        """
        if entity not in ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING:
            print(f"Entity {entity} has no one to one column mapper reference")
            return structure
        # Add one to one relations
        mapper_relation = ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING[entity]
        for relation in mapper_relation:
            column_found = False
            for i in range(len(structure)):
                if relation != structure[i]["name"]:
                    continue
                else:
                    column_found = True

            if not column_found:
                # Specific field not existing as a column, add it
                # ex: commune for address_1.city
                structure.append(
                    {
                        "name": relation,
                        "type": MAPPING_TYPE_TO_UNKNOWN_COLUMN[relation],
                        "multiple": True,
                    }
                )

        return structure

    def add_many_to_x_fields(entity, structure):
        if entity not in ENTITY_TO_COMPLEX_RELATION_MAPPING:
            print(f"Entity {entity} has no many to x relation mapper reference")
            return structure
        # Add other relations (M to O, M to M)
        mapper_complex = ENTITY_TO_COMPLEX_RELATION_MAPPING[entity]
        for (field, type) in mapper_complex.items():
            item = {
                "name": field,
                "type": type,
                "label": f"search.{entity}.fields.{field}",
                "multiple": False,
            }
            structure.append(item)
        return structure

    def add_is_default_fields(entity, structure):
        """
        Add is_default field to each field and position
        """
        if entity not in ENTITY_TO_DEFAULT_MAPPING:
            print(f"Entity {entity} has no is_default column mapper reference")
            # No is_default mapper, all field set to False
            for item in structure:
                item["is_default"] = False
            return structure

        mapper_default = ENTITY_TO_DEFAULT_MAPPING[entity]

        for item in structure:
            item["is_default"] = False
            for column in mapper_default:
                if column == item["name"]:
                    item["is_default"] = True  # Override if found*

            if entity not in MAPPER_ENTITY_TO_ORDER_DEFAULT_FIELDS:
                print(f"Entity {entity} has no order default field mapper reference")
            else:
                for key, order in MAPPER_ENTITY_TO_ORDER_DEFAULT_FIELDS[entity].items():
                    if key == item["name"]:
                        item["order"] = order
        return structure

    def add_enums_values(entity, structure):
        """
        Add enums values to fields which are enums
        """
        if entity not in ENTITY_TO_ENUMS_MAPPING:
            print(f"Entity {entity} has no enums mapper reference")
            return structure

        mapper_enums = ENTITY_TO_ENUMS_MAPPING[entity]
        for item in structure:
            enum_list = []
            for (key, enum_name) in mapper_enums.items():
                enum_list.append(enum_name)
                if key == item["name"]:
                    item["items"] = AppEnumService.get_enums(enum_list)[enum_name]

        return structure

    def add_autocomplete_values(entity, structure):
        """
        Add autocomplete values to fields which must call an endpoint
        """
        if entity not in ENTITY_TO_CONFIG_AUTOCOMPLETE:
            print(f"Entity {entity} has no autocomplete config reference")
            return structure

        autocomplete_config = ENTITY_TO_CONFIG_AUTOCOMPLETE[entity]
        for db_key, config in autocomplete_config.items():

            for elem in structure:
                if elem["name"] == db_key:
                    merge = {**elem, **config}
                    merge["type"] = "autocomplete"
                    structure.remove(elem)
                    structure.append(merge)
        return structure

    def change_column_type(structure):
        """
        Change column type in structure
        to match frontend Input types
        """
        type_mapping = {
            "INTEGER": "number",
            "FLOAT": "number",
            "VARCHAR(255)": "string",
            "TEXT": "string",
            "DATETIME": "date",
            "DATE": "date",
            "BOOLEAN": "boolean",
        }
        for item in structure:
            if item["type"] in type_mapping:
                item["type"] = type_mapping[item["type"]]
            # Specific case for enums values
            if "items" in item:
                item["type"] = "select"
        return structure

    def build_structure(entity, structure):
        """
        Build whole structure
        """
        structure = StructureService.get_structure_from_entity(entity, structure)
        structure = StructureService.add_one_to_one_fields(entity, structure)
        structure = StructureService.add_many_to_x_fields(entity, structure)
        structure = StructureService.add_label_fields(entity, structure)
        structure = StructureService.add_is_default_fields(entity, structure)
        structure = StructureService.add_enums_values(entity, structure)
        structure = StructureService.add_autocomplete_values(entity, structure)

        structure = StructureService.change_column_type(structure)
        return structure


class SearchV2Service:
    def get_one_to_one_references_from_entity(entity):
        """
        Get references from entity
        """
        if entity not in ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING:
            print(f"Entity {entity} has no relation mapper references")
            return None

        return ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING[entity]

    def search_entity(entity, one_to_one_mapper, parameters, operator):
        """
        Build search query from parameters and mapper,
        Perform a recursiv search to manage foreign key columns
        """
        search_obj = SearchV2Service.build_filters_obj(
            one_to_one_mapper, parameters, operator
        )

        # Manage manually complex_filters, ie. Many to One, Many to Many...
        # Filters will be apply as subquery of recursiv search
        complex_filter = ComplexFilters.build_complex_filters(entity, search_obj)

        # Wrapper for apply subquery on search_into_model
        return SearchV2Service.build_querys(entity, search_obj, complex_filter)

    def build_filters_obj(one_to_one_mapper, parameters, operator):
        """
        Build the filters object used by search_into_model recursive query builder
        """
        search = {}
        search["filters"] = []

        for param_column_name, value in parameters.items():
            obj = {}
            obj["values"] = []
            if one_to_one_mapper:
                for column_name, references in one_to_one_mapper.items():
                    # If current column is mapped to a complex field
                    if column_name == param_column_name:
                        obj["field"] = references
            # No mapping found, column is a simple field
            if not "field" in obj:
                obj["field"] = param_column_name

            # Skip term param
            if param_column_name == "term":
                continue

            # Parse the current value to know if it's a list or simple value
            # Manage date differently to allow 'in' and 'range' search
            try:
                value = json.loads(value)
            except ValueError:
                # Here only simple string value
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                    obj["values"].append(value)
                    obj["op"] = "eq"
                    search["filters"].append(obj)
                    continue
                except Exception as e:
                    pass

                # It is a string, not a date, search with IN operator
                obj["values"].append(value)
                obj["op"] = operator
                search["filters"].append(obj)
                continue

            # Here value can be a list or an int
            if isinstance(value, int):
                obj["values"].append(value)
                obj["op"] = "eq"
                search["filters"].append(obj)
                continue

            # Here value is a list
            # Search for range of date
            if len(value) == 2:
                try:
                    datetime.strptime(value[0], "%Y-%m-%d")
                    datetime.strptime(value[1], "%Y-%m-%d")
                    obj["values"] = value
                    obj["op"] = "range"
                    search["filters"].append(obj)
                    continue
                except:
                    pass

            # No range or int found, it's a list of strings, search exact value
            obj["values"] = value
            obj["op"] = "eq"
            search["filters"].append(obj)
        return search

    def build_querys(entity, search_obj, complex_filter):
        """
        Search recursively into model and apply subquery when needed
        """
        # Search recursively from main model
        q = SearchService.search_into_model(ENTITY_TO_MODEL_MAPPING[entity], search_obj)
        # Pass a subquery to perform more filters
        if "syndic_name" in complex_filter:
            q = q.filter(CombinedStructure.id.in_([complex_filter["syndic_name"]]))
        if "owner_name" in complex_filter:
            q = q.filter(Lot.id.in_([complex_filter["owner_name"]]))
        if "mission_id" in complex_filter:
            if entity == "lot":
                q = q.filter(Lot.id.in_([complex_filter["mission_id"]]))
            if entity == "building":
                q = q.filter(Building.id.in_([complex_filter["mission_id"]]))

        return q.all()
