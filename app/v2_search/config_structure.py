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

# Used to know type of fields which are not registered in the database
MAPPING_TYPE_TO_UNKNOWN_COLUMN = {"commune": "string"}


# --------------------------------------------------


# MAPPING ENUMS

MAPPING_MISSION_ENUMS = {"status": "MissionStatus"}

MAPPING_LOT_ENUMS = {"type": "LotType", "occupant_status": "LotOccupantStatus"}

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
