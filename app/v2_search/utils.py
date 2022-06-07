from sqlalchemy import inspect
from app.building.model import Building
from app.copro.copros.model import Copro
from app.lot.model import Lot
import app.mission.permissions as mission_permissions
from app.mission.missions import Mission
from app.mission.teams.service import TeamService
from app.referential.enums.service import AppEnumService
from app.v2_search.config_sql_relations import (
    ENTITY_TO_COMPLEX_RELATION_MAPPING,
    ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING,
)
from app.v2_search.config_structure import (
    ENTITY_TO_CONFIG_AUTOCOMPLETE,
    ENTITY_TO_DEFAULT_MAPPING,
    ENTITY_TO_ENUMS_MAPPING,
    ENTITY_TO_MODEL_MAPPING,
    MAPPER_ENTITY_TO_ORDER_DEFAULT_FIELDS,
    MAPPING_TYPE_TO_UNKNOWN_COLUMN,
)


# STRUCTURE BUILD FUNCTIONS
# --------------------------------------------------


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


def add_label_fields(entity, structure):
    """
    Add i18n label to each field
    """
    for item in structure:
        item["label"] = f"search.{entity}.fields.{item['name']}"
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


# PERMISSION SEARCH FUNCTIONS
# --------------------------------------------------


def filter_by_mission_permission(query, model, user):
    # SC / Copro
    if getattr(model, "mission_id", None):
        query = query.join(Mission, Mission.id == model.mission_id)
    elif model == Building:
        query = query.join(Copro, Copro.id == Building.copro_id)
        query = query.join(Mission, Mission.id == Copro.mission_id)
    elif model == Lot:
        query = query.join(Building, Building.id == Lot.building_id)
        query = query.join(Copro, Copro.id == Building.copro_id)
        query = query.join(Mission, Mission.id == Copro.mission_id)
    return (
        mission_permissions.MissionPermission.filter_query_mission_by_user_permissions(
            query, user
        )
    )


# ADD MISSING INFO FUNCTIONS
# --------------------------------------------------


def add_mission_managers(items):
    for item in items:
        mission_managers = TeamService.get_all_mission_managers(mission_id=item.id)
        item.managers = mission_managers.items
    return items