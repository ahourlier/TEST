from ..mission.missions.model import Mission
from ..lot.model import Lot
from ..building.model import Building
from ..copro.copros.model import Copro
from ..combined_structure.model import CombinedStructure


# - To add a simple field, nothing to do (introspection will search automatically in DB)
# - To add a foreign key, map foreign_key name to the field you want to search (introspection will search automatically in DB)
# - To add a more complex relation:
#    - specify type in config_sql_relations.py
#    - add a query in complex_filters.py and fill complex_filter variable
#    - Verify existence of filter in build_querys in service.py


# MAPPING ENTITY / MODEL

ENTITY_TO_MODEL_MAPPING = {
    "mission": Mission,
    "lot": Lot,
    "building": Building,
    "copro": Copro,
    "combined_structure": CombinedStructure,
}


# --------------------------------------------------


# MAPPING IS_DEFAULT VALUES
# Register each field that must be visible by default
# Register also the order of the fields

MAPPING_MISSION_DEFAULT_COLUMN = ["agency_id", "mission_type", "client_id", "status"]

MAPPING_LOT_DEFAULT_COLUMN = [
    "owner_name",
    "owner_status",
    "type",
    "habitation_type",
    "occupant_status",
]

MAPPING_COPRO_DEFAULT_COLUMN = [
    "commune",
    "address_1_id",
    "address_2_id",
    "syndic_name",
    "priority_copro",
    "construction_time",
    "user_in_charge_id",
]

MAPPING_COMBINED_STRUCTURE_DEFAULT_COLUMN = [
    "type",
    #    "commune",      # -> # TODO LOT 3: Actuellement pas d'adresse
    "name",
    "syndic_name",
]

ENTITY_TO_DEFAULT_MAPPING = {
    "mission": MAPPING_MISSION_DEFAULT_COLUMN,
    "lot": MAPPING_LOT_DEFAULT_COLUMN,
    "copro": MAPPING_COPRO_DEFAULT_COLUMN,
    "combined_structure": MAPPING_COMBINED_STRUCTURE_DEFAULT_COLUMN,
}

ORDER_DEFAULT_FIELDS_MISSION = {
    "agency_id": 1,
    "mission_type": 2,
    "client_id": 3,
    "status": 4,
}

ORDER_DEFAULT_FIELDS_LOT = {
    "owner_name": 1,
    "owner_status": 2,
    "type": 3,
    "habitation_type": 4,
    "occupant_status": 5,
}

ORDER_DEFAULT_FIELDS_COPRO = {
    "commune": 1,
    "address_1_id": 2,
    "address_2_id": 3,
    "syndic_name": 4,
    "priority_copro": 5,
    "construction_time": 6,
    "user_in_charge_id": 7,
}

ORDER_DEFAULT_FIELDS_SC = {
    "type": 1,
    # "commune",
    "name": 2,
    "syndic_name": 3,
}

MAPPER_ENTITY_TO_ORDER_DEFAULT_FIELDS = {
    "mission": ORDER_DEFAULT_FIELDS_MISSION,
    "lot": ORDER_DEFAULT_FIELDS_LOT,
    "copro": ORDER_DEFAULT_FIELDS_COPRO,
    "combined_structure": ORDER_DEFAULT_FIELDS_SC,
}

# Used to know type of fields which are not registered in the database
MAPPING_TYPE_TO_UNKNOWN_COLUMN = {"commune": "string"}


# --------------------------------------------------


# MAPPING ENUMS

MAPPING_MISSION_ENUMS = {"status": "MissionStatus"}

MAPPING_LOT_ENUMS = {"type": "LotType", "habitation_type": "LotHabitationType", "occupant_status": "LotOccupantStatus"}

MAPPING_BUILDING_ENUMS = {"access_type": "AccessType"}

MAPPING_COPRO_ENUMS = {"copro_type": "CoproType"}

MAPPING_COMBINED_STRUCTURE_ENUMS = {"type": "CombinedStructureType"}

ENTITY_TO_ENUMS_MAPPING = {
    "mission": MAPPING_MISSION_ENUMS,
    "lot": MAPPING_LOT_ENUMS,
    "building": MAPPING_BUILDING_ENUMS,
    "copro": MAPPING_COPRO_ENUMS,
    "combined_structure": MAPPING_COMBINED_STRUCTURE_ENUMS,
}


# --------------------------------------------------

# MAPPING AUTOCOMPLETE CONFIGS

AUTOCOMPLETE_MISSION_CONFIG = {
    "antenna_id": {
        "endpointUrl": "/admin/antennas/",
        "fieldsMask": "name,email_address,id",
        "filterFields": ["name", "email_address"],
        "itemValue": "id",
        "itemText": ["name"],
        "title": ["name"],
        "subtitle": ["email_address"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    },
    "agency_id": {
        "endpointUrl": "/admin/agencies/",
        "fieldsMask": "name,id",
        "filterFields": ["name"],
        "itemText": ["name"],
        "title": ["name"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "itemValue": "name",
        "returnObject": True,
    },
    "client_id": {
        "endpointUrl": "/admin/clients/",
        "fieldsMask": "name,last_name,first_name,id",
        "filterFields": ["name", "last_name", "first_name"],
        "itemText": ["name"],
        "title": ["name"],
        "subtitle": ["last_name", "first_name"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "itemValue": "name",
        "returnObject": True,
    },
}

AUTOCOMPLETE_LOT_CONFIG = {
    "building_id": {
        "endpointUrl": "/buildings/",
        "fieldsMask": "name,copro,id",
        "itemValue": "id",
        "itemText": ["name"],
        "filterFields": ["name"],
        "title": ["name"],
        "subtitle": ["copro.name"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    },
    "copro_id": {
        "endpointUrl": "/copro/copros",
        "fieldsMask": "name,copro_type,id",
        "filterFields": ["name", "copro_type"],
        "itemValue": "id",
        "itemText": ["name"],
        "title": ["name"],
        "subtitle": ["copro_type"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    },
}

AUTOCOMPLETE_BUILDING_CONFIG = {
    "copro_id": {
        "endpointUrl": "/copro/copros",
        "fieldsMask": "name,copro_type,id",
        "filterFields": ["name", "copro_type"],
        "itemValue": "id",
        "itemText": ["name"],
        "title": ["name"],
        "subtitle": ["copro_type"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    }
}

AUTOCOMPLETE_COPRO_CONFIG = {
    "cs_id": {
        "endpointUrl": "/combined_structures",
        "fieldsMask": "name,id",
        "filterFields": ["name"],
        "itemValue": "id",
        "itemText": ["name"],
        "title": ["name"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    },
    "mission_id": {
        "endpointUrl": "/mission/missions",
        "fieldsMask": "name,status,id",
        "filterFields": ["name", "status"],
        "itemValue": "id",
        "itemText": ["name"],
        "title": ["name"],
        "subtitle": ["status"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "returnObject": True,
    },
    "user_in_charge_id": {
        "endpointUrl": "/auth/users/",
        "fieldsMask": "first_name, last_name,email,id",
        "filterFields": ["first_name", "last_name", "email"],
        "itemText": ["first_name", "last_name"],
        "title": ["first_name", "last_name"],
        "subtitle": ["email"],
        "cacheItems": True,
        "chips": True,
        "chipsColor": "urbLightGreen",
        "chipsLimit": "50",
        "deletableChips": True,
        "appendIcon": "mdi-magnify",
        "hideNoData": True,
        "itemValue": "name",
        "returnObject": True,
    },
}


ENTITY_TO_CONFIG_AUTOCOMPLETE = {
    "mission": AUTOCOMPLETE_MISSION_CONFIG,
    "lot": AUTOCOMPLETE_LOT_CONFIG,
    "building": AUTOCOMPLETE_BUILDING_CONFIG,
    "copro": AUTOCOMPLETE_COPRO_CONFIG,
}
