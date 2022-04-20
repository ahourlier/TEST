# MAPPING ONE TO ONE RELATIONS

MAPPING_MISSION_SIMPLE_RELATION_TO_FIELD = {
    "agency_id": "agency.name",
    "client_id": "client.name",
}

MAPPING_COPRO_SIMPLE_RELATION_TO_FIELD = {
    "commune": "address_1.city",
    "address_1_id": "address_1.full_address",
    "address_2_id": "address_2.full_address",
    "user_in_charge_id": "user.name",
}

ENTITY_TO_ONE_TO_ONE_RELATION_MAPPING = {
    "mission": MAPPING_MISSION_SIMPLE_RELATION_TO_FIELD,
    "copro": MAPPING_COPRO_SIMPLE_RELATION_TO_FIELD,
}

# --------------------------------------------------

# MAPPING MANY TO X RELATIONS

MAPPING_COMBINED_STRUCTURE_COMPLEX_RELATION = {"syndic_name": "string"}

MAPPING_LOT_COMPLEX_RELATION = {"owner_name": "string"}

ENTITY_TO_COMPLEX_RELATION_MAPPING = {
    "lot": MAPPING_LOT_COMPLEX_RELATION,
    "combined_structure": MAPPING_COMBINED_STRUCTURE_COMPLEX_RELATION,
}
