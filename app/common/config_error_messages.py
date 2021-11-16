INCONSISTENT_UPDATE_ID_DEFAULT = "The provided id is conflicting with body object id"
KEY_INCONSISTENT_UPDATE_ID_DEFAULT = "INCONSISTENT_UPDATE_ID_EXCEPTION"

AGENCY_NOT_FOUND_EXCEPTION = "Could not find an agency with this id"
KEY_AGENCY_NOT_FOUND_EXCEPTION = "AGENCY_NOT_FOUND_EXCEPTION"

ANTENNA_NOT_FOUND_EXCEPTION = "Could not find an antenna with this id"
KEY_ANTENNA_NOT_FOUND_EXCEPTION = "ANTENNA_NOT_FOUND_EXCEPTION"

USER_NOT_FOUND_EXCEPTION = "Could not find a user with this id"
KEY_USER_NOT_FOUND_EXCEPTION = "USER_NOT_FOUND_EXCEPTION"

UNKNOWN_CONNEXION_EMAIL = "Provided email does not match any registered user"
KEY_UNKNOWN_CONNEXION_EMAIL = "UNKNOWN_CONNEXION_EMAIL"

INACTIVE_USER = "Authentified user is not active"
KEY_INACTIVE_USER = "INACTIVE_USER"

CLIENT_NOT_FOUND_EXCEPTION = "Could not find a client with this id"
KEY_CLIENT_NOT_FOUND_EXCEPTION = "CLIENT_NOT_FOUND_EXCEPTION"

CHILD_MISSION_EXCEPTION = "At least one mission is linked to this entity"
KEY_CHILD_MISSION_EXCEPTION = "CHILD_MISSION_EXCEPTION"

MISSION_NOT_FOUND_EXCEPTION = "Could not find a mission with this id"
KEY_MISSION_NOT_FOUND_EXCEPTION = "MISSION_NOT_FOUND_EXCEPTION"

TEAM_NOT_FOUND_EXCEPTION = "Could not find a team association with this id"
KEY_TEAM_NOT_FOUND_EXCEPTION = "TEAM_NOT_FOUND_EXCEPTION"

DOCUMENT_NOT_FOUND_EXCEPTION = "Could not find a document with this id"
KEY_DOCUMENT_NOT_FOUND_EXCEPTION = "DOCUMENT_NOT_FOUND_EXCEPTION"

PROJECT_NOT_FOUND_EXCEPTION = "Could not find a project with this id"
KEY_PROJECT_NOT_FOUND_EXCEPTION = "PROJECT_NOT_FOUND_EXCEPTION"

REQUESTER_NOT_FOUND_EXCEPTION = "Could not find a requester with this id"
KEY_REQUESTER_NOT_FOUND_EXCEPTION = "REQUESTER_NOT_FOUND_EXCEPTION"

CONTACT_NOT_FOUND_EXCEPTION = "Could not find a contact with this id"
KEY_CONTACT_NOT_FOUND_EXCEPTION = "CONTACT_NOT_FOUND_EXCEPTION"

TAXABLE_INCOME_NOT_FOUND_EXCEPTION = "Could not find a taxable income with this id"
KEY_TAXABLE_INCOME_NOT_FOUND_EXCEPTION = "TAXABLE_INCOME_NOT_FOUND_EXCEPTION"

CHILD_ANTENNA_EXCEPTION = "At least one antenna is linked to this agency"
KEY_CHILD_ANTENNA_EXCEPTION = "CHILD_ANTENNA_EXCEPTION"

PROJECT_LEAD_NOT_FOUND_EXCEPTION = "Could not find a project lead relation with this id"
KEY_PROJECT_LEAD_NOT_FOUND_EXCEPTION = "PROJECT_LEAD_NOT_FOUND_EXCEPTION"

ACCOMMODATION_NOT_FOUND_EXCEPTION = (
    "Could not find an accommodation lead relation with this id"
)
KEY_ACCOMMODATION_NOT_FOUND_EXCEPTION = "ACCOMMODATION_LEAD_NOT_FOUND_EXCEPTION"

DISORDER_NOT_FOUND_EXCEPTION = "Could not find a disorder lead relation with this id"
KEY_DISORDER_NOT_FOUND_EXCEPTION = "DISORDER_LEAD_NOT_FOUND_EXCEPTION"

DISORDER_TYPE_NOT_FOUND_EXCEPTION = (
    "Could not find a disorder type lead relation with this id"
)

INVALID_DISORDER_JOINS_EXCEPTION = (
    "Disorders cannot be joined both with an accommodation and a common_area"
)
KEY_INVALID_DISORDER_JOINS_EXCEPTION = "INVALID_DISORDER_JOINS_EXCEPTION"

KEY_DISORDER_TYPE_NOT_FOUND_EXCEPTION = "DISORDER_TYPE_LEAD_NOT_FOUND_EXCEPTION"

INVALID_SEARCH_OPERATOR_EXCEPTION = "Provided search operator is invalid."
KEY_INVALID_SEARCH_OPERATOR_EXCEPTION = "INVALID_SEARCH_OPERATOR_EXCEPTION"

INVALID_SEARCH_FIELD_EXCEPTION = "Provided search field does not match any valid field."
KEY_INVALID_SEARCH_FIELD_EXCEPTION = "INVALID_SEARCH_FIELD_EXCEPTION"

AGENCY_DUPLICATE_NAME_EXCEPTION = "An agency with this name already exists."
KEY_AGENCY_DUPLICATE_NAME_EXCEPTION = "AGENCY_DUPLICATE_NAME_EXCEPTION"

ANTENNA_DUPLICATE_NAME_EXCEPTION = "An antenna with this name already exists."
KEY_ANTENNA_DUPLICATE_NAME_EXCEPTION = "ANTENNA_DUPLICATE_NAME_EXCEPTION"

SEARCH_NOT_FOUND_EXCEPTION = "Could not find a search with this id"
KEY_SEARCH_NOT_FOUND_EXCEPTION = "SEARCH_NOT_FOUND_EXCEPTION"

COMMENT_NOT_FOUND_EXCEPTION = "Could not find a comment with this id"
KEY_COMMENT_NOT_FOUND_EXCEPTION = "COMMENT_NOT_FOUND_EXCEPTION"

FORBIDDEN_EXCEPTION = "Authenticated user does not have permission to access this data."
KEY_FORBIDDEN_EXCEPTION = "FORBIDDEN_EXCEPTION"

UNIDENTIFIED_REFERRER_EXCEPTION = "Provided referrer does not have an id."
KEY_UNIDENTIFIED_REFERRER_EXCEPTION = "UNIDENTIFIED_REFERRER_EXCEPTION"

FUNDER_NOT_FOUND_EXCEPTION = "Could not find a funder with this id"
KEY_FUNDER_NOT_FOUND_EXCEPTION = "FUNDER_NOT_FOUND_EXCEPTION"

FUNDER_MISSION_CHANGE_EXCEPTION = (
    "A funder cannot be detached from a mission or attached to a different mission"
)
KEY_FUNDER_MISSION_CHANGE_EXCEPTION = "FUNDER_MISSION_CHANGE_EXCEPTIOn"

FUNDING_SCENARIO_NOT_FOUND_EXCEPTION = "Could not find a funding scenario with this id"
KEY_FUNDING_SCENARIO_NOT_FOUND_EXCEPTION = "FUNDING_SCENARIO_NOT_FOUND_EXCEPTION"

FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION = "A funding scenario cannot be detached from a funder or attached to a different funder"
KEY_FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION = (
    "FUNDING_SCENARIO_FUNDER_CHANGE_EXCEPTION"
)

CHILD_CLIENT_MISSION_EXCEPTION = "At least one mission is linked to this client"
KEY_CHILD_CLIENT_MISSION_EXCEPTION = "CHILD_CLIENT_MISSION_EXCEPTION"

CHILD_ANTENNA_MISSION_EXCEPTION = "At least one mission is linked to this antenna"
KEY_CHILD_ANTENNA_MISSION_EXCEPTION = "CHILD_ANTENNA_MISSION_EXCEPTION"

CHILD_AGENCY_MISSION_EXCEPTION = "At least one mission is linked to this agency"
KEY_CHILD_AGENCY__MISSION_EXCEPTION = "CHILD_AGENCY_MISSION_EXCEPTION"

WORK_TYPE_NOT_FOUND_EXCEPTION = "Could not find a work type with this id"
KEY_WORK_TYPE_NOT_FOUND_EXCEPTION = "WORK_TYPE_NOT_FOUND_EXCEPTION"

KEY_FUNDING_SCENARIO_INVALID_RATE = "FUNDING_SCENARIO_INVALID_RATE_EXCEPTION"
KEY_FUNDING_SCENARIO_INVALID_CRITERIA = "FUNDING_SCENARIO_INVALID_CRITERIA"

VALIDATION_ERRORS = {
    KEY_FUNDING_SCENARIO_INVALID_RATE: "Rate should be between 0 and 100.",
    KEY_FUNDING_SCENARIO_INVALID_CRITERIA: "Invalid criteria format.",
}

QUOTE_NOT_FOUND_EXCEPTION = "Could not find a quote with this id"
KEY_QUOTE_NOT_FOUND_EXCEPTION = "QUOTE_NOT_FOUND_EXCEPTION"

SIMULATION_NOT_FOUND_EXCEPTION = "Could not find a simulation with this id"
KEY_SIMULATION_NOT_FOUND_EXCEPTION = "SIMULATION_NOT_FOUND_EXCEPTION"

USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation use case with this id"
)
KEY_USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION = "USE_CASE_SIMULATION_NOT_FOUND_EXCEPTION"

SIMULATION_QUOTE_NOT_FOUND_EXCEPTION = "Could not find a simulation_quote with this id"
KEY_SIMULATION_QUOTE_NOT_FOUND_EXCEPTION = "SIMULATION_QUOTE_NOT_FOUND_EXCEPTION"

SIMULATION_FUNDER_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation_funder with this id"
)
KEY_SIMULATION_FUNDER_NOT_FOUND_EXCEPTION = "SIMULATION_FUNDER_NOT_FOUND_EXCEPTION"

SIMULATION_USED_EXCEPTION = "This simulation is used and cannot be deleted"
KEY_SIMULATION_USED_EXCEPTION = "SIMULATION_USED_EXCEPTION"

CLONE_FUNDER_EXCEPTION = "This funder is already a clone from an existing simulation"
KEY_CLONE_FUNDER_EXCEPTION = "CLONE_FUNDER_EXCEPTION"

KEY_SHARED_DRIVE_CREATION_EXCEPTION = "SHARED_DRIVE_CREATION_EXCEPTION"
KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION = "SHARED_DRIVE_FOLDER_CREATION_EXCEPTION"
KEY_SHARED_DRIVE_PERMISSION_EXCEPTION = "SHARED_DRIVE_PERMISSION_EXCEPTION"
KEY_SHARED_DRIVE_RENAME_EXCEPTION = "SHARED_DRIVE_RENAME_EXCEPTION"
KEY_SHARED_DRIVE_COPY_EXCEPTION = "SHARED_DRIVE_COPY_EXCEPTION"
KEY_SHARED_DRIVE_FETCH_EXCEPTION = "SHARED_DRIVE_FETCH_EXCEPTION"

SHARED_DRIVE_ERRORS = {
    KEY_SHARED_DRIVE_CREATION_EXCEPTION: "Unable to create shared drive.",
    KEY_SHARED_DRIVE_FOLDER_CREATION_EXCEPTION: "Unable to create folder in shared drive",
    KEY_SHARED_DRIVE_PERMISSION_EXCEPTION: "Error while managing Shared Drive permissions.",
    KEY_SHARED_DRIVE_COPY_EXCEPTION: "Unable to copy document to shared drive.",
    KEY_SHARED_DRIVE_RENAME_EXCEPTION: "Unable to rename shared drive file.",
    KEY_SHARED_DRIVE_FETCH_EXCEPTION: "Unable to fetch shared drive file.",
}

KEY_GOOGLE_DOCS_GET_EXCEPTION = "GOOGLE_DOCS_GET_EXCEPTION"
KEY_GOOGLE_DOCS_UPDATE_EXCEPTION = "GOOGLE_DOCS_UPDATE_EXCEPTION"
KEY_GOOGLE_DOCS_INVALID_FILE_EXCEPTION = "GOOGLE_DOCS_INVALID_FILE_EXCEPTION"

GOOGLE_DOCS_ERRORS = {
    KEY_GOOGLE_DOCS_GET_EXCEPTION: "Unable to get google docs.",
    KEY_GOOGLE_DOCS_UPDATE_EXCEPTION: "Unable to update google docs.",
    KEY_GOOGLE_DOCS_INVALID_FILE_EXCEPTION: "Invalid template type",
}

KEY_GOOGLE_SHEETS_GET_EXCEPTION = "GOOGLE_SHEETS_GET_EXCEPTION"
KEY_GOOGLE_SHEETS_UPDATE_EXCEPTION = "GOOGLE_SHEETS_UPDATE_EXCEPTION"
KEY_GOOGLE_SHEETS_INVALID_FILE_EXCEPTION = "GOOGLE_SHEETS_INVALID_FILE_EXCEPTION"

GOOGLE_SHEETS_ERRORS = {
    KEY_GOOGLE_SHEETS_GET_EXCEPTION: "Unable to get google sheets.",
    KEY_GOOGLE_SHEETS_UPDATE_EXCEPTION: "Unable to update google sheets.",
    KEY_GOOGLE_SHEETS_INVALID_FILE_EXCEPTION: "Invalid template type",
}

KEY_GOOGLE_GROUP_CREATION_EXCEPTION = "GOOGLE_GROUP_CREATION_EXCEPTION"
KEY_GOOGLE_GROUP_MEMBERSHIP_EXCEPTION = "GOOGLE_GROUP_MEMBERSHIP_EXCEPTION"
KEY_GOOGLE_GROUP_VISIBILITY_CHANGE_EXCEPTION = (
    "GOOGLE_GROUP_VISIBILITY_CHANGE_EXCEPTION"
)

GOOGLE_GROUPS_ERRORS = {
    KEY_GOOGLE_GROUP_CREATION_EXCEPTION: "Unable to create Google Group.",
    KEY_GOOGLE_GROUP_MEMBERSHIP_EXCEPTION: "Error while managing Google Group members.",
    KEY_GOOGLE_GROUP_VISIBILITY_CHANGE_EXCEPTION: "Error while setting Group visibility to private.",
}

SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation_deposit with this id"
)
KEY_SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION = "SIMULATION_DEPOSIT_NOT_FOUND_EXCEPTION"

SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation payment request with this id"
)
KEY_SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION = (
    "SIMULATION_PAYMENT_REQUEST_NOT_FOUND_EXCEPTION"
)

SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation_certified with this id"
)
KEY_SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION = (
    "SIMULATION_CERTIFIED_NOT_FOUND_EXCEPTION"
)

SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation sub result with this id"
)
KEY_SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION = (
    "SIMULATION_SUB_RESULT_NOT_FOUND_EXCEPTION"
)

FUNDER_USED_BY_SIMULATION_EXCEPTION = (
    "This funder is linked to a simulation and cannot be deleted"
)
KEY_FUNDER_USED_BY_SIMULATION_EXCEPTION = "FUNDER_USED_BY_SIMULATION"

REQUESTER_TYPE_CONSTANT_EXCEPTION = "The requester type cannot be modified"
KEY_REQUESTER_TYPE_CONSTANT_EXCEPTION = "REQUESTER_TYPE_CONSTANT_EXCEPTION"

COMMON_AREA_NOT_FOUND_EXCEPTION = "Could not find a common_area entity with this id"
KEY_COMMON_AREA_NOT_FOUND_EXCEPTION = "COMMON_AREA_NOT_FOUND_EXCEPTION"

EXISTING_COMMON_AREA_EXCEPTION = (
    "This project already has a common area entity. Use PUT instead"
)
KEY_EXISTING_COMMON_AREA_EXCEPTION = "EXISTING_COMMON_AREA_EXCEPTION"

INVALID_PARAMS_REQUEST_EXCEPTION = "Invalid request parameters for this endpoint"
KEY_INVALID_PARAMS_REQUEST_EXCEPTION = "INVALID_PARAMS_REQUEST_EXCEPTION"

QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION = (
    "Could not find a quote_accommodation entity with this id"
)
KEY_QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION = "QUOTE_ACCOMMODATION_NOT_FOUND_EXCEPTION"

SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION = (
    "Could not find a simulation_accommodation entity with this id"
)
KEY_SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION = (
    "SIMULATION_ACCOMMODATION_NOT_FOUND_EXCEPTION"
)

FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION = (
    "Could not find a funder_accommodations entity with this id"
)
KEY_FUNDER_ACCOMMODATIONS_NOT_FOUND_EXCEPTION = (
    "SIMULATION_ACCOMMODATIONS_NOT_FOUND_EXCEPTION"
)

ACCOMMODATION_ALREADY_USED_EXCEPTION = (
    "This accommodation is already used in this simulation"
)
KEY_ACCOMMODATION_ALREADY_USED_EXCEPTION = "ACCOMMODATION_ALREADY_USED_EXCEPTION"

CUSTOM_FIELD_NOT_FOUND_EXCEPTION = "Could not find a custom_field entity with this id"
KEY_CUSTOM_FIELD_NOT_FOUND_EXCEPTION = "CUSTOM_FIELD_NOT_FOUND_EXCEPTION"

PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION = (
    "Could not find a project_custom_field entity with this id"
)
KEY_PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION = (
    "PROJECT_CUSTOM_FIELD_NOT_FOUND_EXCEPTION"
)

CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION = (
    "Could not find a custom_field_value entity with this id"
)
KEY_CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION = "CUSTOM_FIELD_VALUE_NOT_FOUND_EXCEPTION"

AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION = (
    "Could not find an available_field_value entity with this id"
)
KEY_AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION = (
    "AVAILABLE_FIELD_VALUE_NOT_FOUND_EXCEPTION"
)

MONITOR_NOT_FOUND_EXCEPTION = "Could not find a monitor entity with this id"
KEY_MONITOR_NOT_FOUND_EXCEPTION = "MONITOR_NOT_FOUND_EXCEPTION"

MONITOR_FIELD_NOT_FOUND_EXCEPTION = "Could not find a monitor_field entity with this id"
KEY_MONITOR_FIELD_NOT_FOUND_EXCEPTION = "MONITOR_FIELD_NOT_FOUND_EXCEPTION"


FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION = (
    "Could not find a funder_monitoring_value entity with this id"
)
KEY_FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION = (
    "FUNDER_MONITORING_VALUE_NOT_FOUND_EXCEPTION"
)

# EMAILS

EMAIL_NOT_FOUND_EXCEPTION = "Could not find an email with this id"
KEY_EMAIL_NOT_FOUND_EXCEPTION = "EMAIL_NOT_FOUND_EXCEPTION"

EMAIL_MISSING_RECIPIENT_EXCEPTION = (
    "You need to provide at least one recipient in to, cc or bcc fields."
)
KEY_EMAIL_MISSING_RECIPIENT_EXCEPTION = "EMAIL_MISSING_RECIPIENT_EXCEPTION"

EMAIL_NOT_INTERNAL_SENDER_EXCEPTION = "Only internal users are allowed to send emails."
KEY_EMAIL_NOT_INTERNAL_SENDER_EXCEPTION = "EMAIL_NOT_INTERNAL_SENDER_EXCEPTION"

INVALID_SOURCE_EXCEPTION = "Invalid source for this document"
KEY_INVALID_SOURCE_EXCEPTION = "INVALID_SOURCE_EXCEPTION"

DATA_IMPORT_NOT_FOUND_EXCEPTION = "Could not find a data import with this id"
KEY_DATA_IMPORT_NOT_FOUND_EXCEPTION = "DATA_IMPORT_NOT_FOUND_EXCEPTION"

INCORRECT_DATA_IMPORT_EXCEPTION = "Incorrect format data provided for importation"
KEY_INCORRECT_DATA_IMPORT_EXCEPTION = "INCORRECT_DATA_IMPORT_EXCEPTION"

ENTITY_INSERT_FAIL_EXCEPTION = "Provided data could not be inserted into database"
KEY_ENTITY_INSERT_FAIL_EXCEPTION = "ENTITY_INSERT_FAIL_EXCEPTION"

# PERRENOUD

SCENARIO_NOT_FOUND_EXCEPTION = "Could not find a scenario with this id"
KEY_SCENARIO_NOT_FOUND_EXCEPTION = "SCENARIO_NOT_FOUND_EXCEPTION"

HEATING_NOT_FOUND_EXCEPTION = "Could not find a heating with this id"
KEY_HEATING_NOT_FOUND_EXCEPTION = "HEATING_NOT_FOUND_EXCEPTION"

HOT_WATER_NOT_FOUND_EXCEPTION = "Could not find an hot_water with this id"
KEY_HOT_WATER_NOT_FOUND_EXCEPTION = "HOT_WATER_NOT_FOUND_EXCEPTION"

OUTSIDE_WALL_NOT_FOUND_EXCEPTION = "Could not find an outside wall with this id"
KEY_OUTSIDE_WALL_NOT_FOUND_EXCEPTION = "OUTSIDE_WALL_NOT_FOUND_EXCEPTION"

WOODWORK_NOT_FOUND_EXCEPTION = "Could not find a woodwork with this id"
KEY_WOODWORK_NOT_FOUND_EXCEPTION = "WOODWORK_NOT_FOUND_EXCEPTION"

CEILING_NOT_FOUND_EXCEPTION = "Could not find a ceiling with this id"
KEY_CEILING_NOT_FOUND_EXCEPTION = "CEILING_NOT_FOUND_EXCEPTION"

FLOOR_NOT_FOUND_EXCEPTION = "Could not find a floo with this id"
KEY_FLOOR_NOT_FOUND_EXCEPTION = "FLOOR_NOT_FOUND_EXCEPTION"

THERMAL_BRIDGE_NOT_FOUND_EXCEPTION = "Could not find a thermal bridge with this id"
KEY_THERMAL_BRIDGE_NOT_FOUND_EXCEPTION = "THERMAL_BRIDGE_NOT_FOUND_EXCEPTION"

AREA_NOT_FOUND_EXCEPTION = "Could not find an area with this id"
KEY_AREA_NOT_FOUND_EXCEPTION = "AREA_NOT_FOUND_EXCEPTION"

ROOM_NOT_FOUND_EXCEPTION = "Could not find a room with this id"
KEY_ROOM_NOT_FOUND_EXCEPTION = "ROOM_NOT_FOUND_EXCEPTION"

ROOM_INPUT_NOT_FOUND_EXCEPTION = "Could not find a room_input with this id"
KEY_ROOM_INPUT_NOT_FOUND_EXCEPTION = "ROOM_INPUT_NOT_FOUND_EXCEPTION"

PHOTO_NOT_FOUND_EXCEPTION = "Could not find a photo with this id"
KEY_PHOTO_NOT_FOUND_EXCEPTION = "PHOTO_NOT_FOUND_EXCEPTION"

INVALID_ROOM_INPUT_KIND_EXCEPTION = "Invalid room input kind"
KEY_INVALID_ROOM_INPUT_KIND_EXCEPTION = "INVALID_ROOM_INPUT_KIND_EXCEPTION"

EXISTING_INITIAL_STATE_EXCEPTION = (
    "An initial state already exist for this accommodation"
)
KEY_EXISTING_INITIAL_STATE_EXCEPTION = "EXISTING_INITIAL_STATE_EXCEPTION"


KEY_XML_MISSING_ROOT_EXCEPTION = "XML_MISSING_ROOT_EXCEPTION"
KEY_XML_CONFLICTING_ROOTS_EXCEPTION = "XML_CONFLICTING_ROOTS_EXCEPTION"
KEY_XML_MISSING_CONFIGURATION_INFOS_EXCEPTION = (
    "XML_MISSING_CONFIGURATION_FIELDS_EXCEPTION"
)
KEY_XML_MISSING_CONFIGURATION_FIELDS = "XML_MISSING_CONFIGURATION_FIELDS"
KEY_XML_INVALID_ITERATION_PARENT = "XML_INVALID_ITERATION_PARENT"

XML_GENERATION_ERRORS = {
    KEY_XML_MISSING_ROOT_EXCEPTION: "First element of the XML configuration is not marked as 'is_root'.",
    KEY_XML_CONFLICTING_ROOTS_EXCEPTION: "XML configuration file contains two conflicting roots.",
    KEY_XML_MISSING_CONFIGURATION_INFOS_EXCEPTION: "At least one mandatory field is missing in the XML configuration. (Could be 'id', 'tag', or 'parent')",
    KEY_XML_MISSING_CONFIGURATION_FIELDS: "An XML configuration item does not have mandatory fields",
    KEY_XML_INVALID_ITERATION_PARENT: "The XML iteration parent has been badly mapped (it does not contains a proper instances list)",
}


APP_CONFIG_NOT_FOUND_EXCEPTION = "No application configuration element found"
KEY_APP_CONFIG_NOT_FOUND_EXCEPTION = "APP_CONFIG_NOT_FOUND_EXCEPTION"

INVALID_PHOTO_CONTEXT_EXCEPTION = "Request does not contain valid photo context data"
KEY_INVALID_PHOTO_CONTEXT_EXCEPTION = "INVALID_PHOTO_CONTEXT_EXCEPTION"

MISSING_PHOTO_EXCEPTION = "Request does not contain any valid photo to upload"
KEY_MISSING_PHOTO_EXCEPTION = "MISSING_PHOTO_EXCEPTION"

MISSING_NAME_EXCEPTION = "Request does not contain any valid photo name"
KEY_MISSING_NAME_EXCEPTION = "MISSING_NAME_EXCEPTION"

MISSING_SECTION_EXCEPTION = "Request does not contain any valid upload section"
KEY_MISSING_SECTION_EXCEPTION = "MISSING_SECTION_EXCEPTION"

MISSING_ROOM_EXCEPTION = "Request does not contain any valid room name"
KEY_MISSING_ROOM_EXCEPTION = "MISSING_ROOM_EXCEPTION"

INVALID_FILE_EXCEPTION = "Provided file has wrong name or invalid size"
KEY_INVALID_FILE_EXCEPTION = "INVALID_FILE_EXCEPTION"

TYPE_ROOM_INPUT_IN_USE_EXCEPTION = (
    "An input with this metric type already exists in the parent room"
)
KEY_TYPE_ROOM_INPUT_IN_USE_EXCEPTION = "TYPE_ROOM_INPUT_IN_USE_EXCEPTION"

PERRENOUD_WEBSERVICE_EXCEPTION = (
    "An error occured while parsing the Perrenoud WebService response"
)
KEY_PERRENOUD_WEBSERVICE_EXCEPTION = "PERRENOUD_WEBSERVICE_EXCEPTION"

MISSING_PERRENOUD_DATA_EXCEPTION = (
    "Perrenoud Analysis failed due to missing Perrenoud Data"
)
KEY_MISSING_PERRENOUD_DATA_EXCEPTION = "MISSING_PERRENOUD_DATA_EXCEPTION"

PREFERRED_APP_NOT_FOUND = "Could not determine preferred app"
KEY_PREFERRED_APP_NOT_FOUND = (
    "PREFERRED_APP_NOT_FOUND_EXCEPTION"  # todo add in translation
)

REFERENT_NOT_FOUND_EXCEPTION = "Could not find a referent with this id"
KEY_REFERENT_NOT_FOUND_EXCEPTION = (
    "REFERENT_NOT_FOUND_EXCEPTION"  # todo add in translation
)

UNKNOWN_MISSION_TYPE_EXCEPTION = "Mission type unknown"  # todo add in translation
KEY_UNKNOWN_MISSION_TYPE_EXCEPTION = "UNKNOWN_MISSION_TYPE_EXCEPTION"

MISSION_DETAIL_NOT_FOUND_EXCEPTION = "Could not find a mission detail with this id"
KEY_MISSION_DETAIL_NOT_FOUND_EXCEPTION = (
    "MISSION_DETAIL_NOT_FOUND_EXCEPTION"  # todo add in translation
)

PARTNER_NOT_FOUND_EXCEPTION = "Partner not found"  # todo add in translation
KEY_PARTNER_NOT_FOUND_EXCEPTION = "PARTNER_NOT_FOUND_EXCEPTION"

SUBCONTRACTOR_NOT_FOUND_EXCEPTION = "Subcontractor not found"  # todo add in translation
KEY_SUBCONTRACTOR_NOT_FOUND_EXCEPTION = "SUBCONTRACTOR_NOT_FOUND_EXCEPTION"

ELECT_NOT_FOUND_EXCEPTION = "Elect not found"  # todo add in translation
KEY_ELECT_NOT_FOUND_EXCEPTION = "ELECT_NOT_FOUND_EXCEPTION"

COPRO_NOT_FOUND_EXCEPTION = "Could not find a copro with this id"  # todo add in translation
KEY_COPRO_NOT_FOUND_EXCEPTION = "COPRO_NOT_FOUND_EXCEPTION"

MISSION_NOT_TYPE_COPRO_EXCEPTION = "Unable to create copro in this mission: not a type Copro"  # todo add in translation
KEY_MISSION_NOT_TYPE_COPRO_EXCEPTION = "MISSION_NOT_TYPE_COPRO_EXCEPTION"
