DEFAULT_FIELDS = [
    {"name": "version_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "thematique_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "resource_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "version_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "version_date", "type": "DATE", "mode": "NULLABLE"},
    {"name": "step_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "step_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "step_status", "type": "STRING", "mode": "NULLABLE"},
]

FIELDS_MAPPING = {
    "group": "RECORD",
    "string": "STRING",
    "currency": "NUMERIC",
    "select": "STRING",
    "date": "DATE",
    "textArea": "STRING",
    "switch": "BOOLEAN",
    "phone": "RECORD",
    "email": "STRING",
    "number": "NUMERIC",
    "select_multiple": "STRING",
    "telephone": "RECORD",
    "autocomplete": "RECORD",
    "autocomplete_multiple": "RECORD",
    "password": "STRING",
    "address": "RECORD",
}

BQ_DATASET = "firestore_export"

BQ_SCHEMA_TEL = [
    {"name": "countryCode", "type": "STRING", "mode": "NULLABLE"},
    {"name": "formatInternational", "type": "STRING", "mode": "NULLABLE"},
    {"name": "formatNational", "type": "STRING", "mode": "NULLABLE"},
]

BQ_SCHEMA_ADDRESS = [
    {"name": "additional_info", "type": "STRING", "mode": "NULLABLE"},
    {"name": "city", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_at", "type": "DATETIME", "mode": "NULLABLE"},
    {"name": "full_address", "type": "STRING", "mode": "NULLABLE"},
    {"name": "id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "number", "type": "STRING", "mode": "NULLABLE"},
    {"name": "postal_code", "type": "STRING", "mode": "NULLABLE"},
    {"name": "street", "type": "STRING", "mode": "NULLABLE"},
    {"name": "updated_at", "type": "DATETIME", "mode": "NULLABLE"},
]

BQ_SCHEMA_FINANCEUR = [
    {"name": "created_at", "type": "DATETIME", "mode": "NULLABLE"},
    {"name": "updated_at", "type": "DATETIME", "mode": "NULLABLE"},
    {"name": "position", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "is_deleted", "type": "BOOLEAN", "mode": "NULLABLE"},
    {"name": "is_national", "type": "BOOLEAN", "mode": "NULLABLE"},
    {"name": "is_duplicate", "type": "BOOLEAN", "mode": "NULLABLE"},
    {"name": "subvention_round", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "priority", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "type", "type": "STRING", "mode": "NULLABLE"},
    {"name": "requester_type", "type": "STRING", "mode": "NULLABLE"},
    {"name": "mission_id", "type": "INTEGER", "mode": "NULLABLE"},
]
