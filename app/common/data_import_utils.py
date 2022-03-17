import datetime
from enum import Enum

from flask_restx import abort

from app.auth.users.model import UserRole
from app.common.constants import FRENCH_DATE_FORMAT
from app.common.sheets_util import SheetsUtils


class SheetFieldsTypes(Enum):
    STRING = "str"
    INTEGER = "int"
    BOOLEAN = "bool"
    FLOAT = "float"
    PHONE = "phone_number"
    DATE_DAY = "date_day"
    DATE_YEAR = "date_year"
    PRIMARY_ID = "primary_sheet_id"
    FOREIGN_ID = "foreign_sheet_id"
    DISORDER_TYPE = "disorder_type"
    WORK_TYPE = "work_type"
    ANALYSIS = "analysis"
    RECOMMMENDATION = "recommendation"
    USER_EMAIL = "user_email"


BOOLEAN_VALID_VALUES = {"OUI": True, "NON": False}


class BaseEntities(Enum):
    PROJECT = "Project"
    REQUESTER = "Requester"
    CONTACT = "Contact"
    TAXABLE_INCOME = "TaxableIncome"
    ACCOMMODATION = "Accommodation"
    PHONE_NUMBER = "PhoneNumber"
    DISORDER = "Disorder"
    DISORDER_TYPE = "DisorderType"
    COMMON_AREA = "CommonArea"
    PROJECT_LEAD = "ProjectLead"
    WORK_TYPE = "WorkType"


class SheetsList(Enum):
    PROJECTS = "Projets"
    REQUESTERS = "Demandeurs"
    TAXABLE_INCOME = "Revenu_Fiscal_De_Reference"
    CONTACTS = "Contacts"
    ACCOMMODATIONS = "Logements"
    DISORDERS = "Constats_Recommandations"
    COMMON_AREA = "Parties_Communes"
    PROJECTS_LEADS = "Referents"


date_status_fields_map = {
    "Visite conseil à programmer": "date_meet_advices_to_plan",
    "Visite contrôle à programmer": "date_meet_control_to_plan",
    "Demande de payement à faire": "date_asking_for_pay",
    "En cours de montage": "date_build_on_going",
    "Agrée": "date_certified",
    "Soldé": "date_cleared",
    "Contact": "date_contact",
    "Déposé": "date_depositted",
    "Sans suite": "date_dismissed",
    "Visite contrôle programmée": "date_meet_control_planned",
    "Visite conseil programmée": "date_meet_advices_planned",
    "Visite à traiter": "date_meet_to_process",
    "Non éligible": "date_non_eligible",
    "Demande paiement à faire": "date_payment_request_to_do",
    "À Contacter": "date_to_contact",
}

projects_fields_map = {
    "identifiant du projet": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.PROJECT.value,
    },
    "identifiant du demandeur associé": {
        "field": "requester_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.PROJECT.value,
        "foreign_model": BaseEntities.REQUESTER.value,
        "key_in_foreign_table": "id",
    },
    "identifiant de la mission associée": {
        "field": "mission_id",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.PROJECT.value,
    },
    "status": {
        "field": "status",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "adresse": {
        "field": "address",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "numéro de rue": {
        "field": "address_number",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "rue": {
        "field": "address_street",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "code postal": {
        "field": "address_code",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "commune": {
        "field": "address_location",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "complément": {
        "field": "address_complement",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "type de dossier": {
        "field": "type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "type de dossier secondaire": {
        "field": "secondary_case_type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "types de travaux": {
        "type": SheetFieldsTypes.WORK_TYPE.value,
        "model": BaseEntities.PROJECT.value,
    },
    "description": {
        "field": "description",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "projet sans suite": {
        "field": "closed",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.PROJECT.value,
    },
    "raison projet sans suite": {
        "field": "closure_motive",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "visite urgente": {
        "field": "urgent_visit",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.PROJECT.value,
    },
    "date de visite conseil": {
        "field": "date_advice_meet",
        "type": SheetFieldsTypes.DATE_DAY.value,
        "model": BaseEntities.PROJECT.value,
    },
    "date de visite de contrôle": {
        "field": "date_control_meet",
        "type": SheetFieldsTypes.DATE_DAY.value,
        "model": BaseEntities.PROJECT.value,
    },
    "notes de suivi": {
        "field": "notes",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "pas de demande d'avance": {
        "field": "no_advance_request",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.PROJECT.value,
    },
    "commentaire": {
        "field": "monitoring_commentary",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.PROJECT.value,
    },
    "actif": {
        "field": "active",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.PROJECT.value,
    },
}

requesters_fields_map = {
    "identifiant du demandeur": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "email": {
        "field": "email",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "prenom": {
        "field": "first_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "nom": {
        "field": "last_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "civilité": {
        "field": "title",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "date de naissance": {
        "field": "birthday_date",
        "type": SheetFieldsTypes.DATE_DAY.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "téléphone_1": {
        "field": "phone_number",
        "type": SheetFieldsTypes.PHONE.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "téléphone_2": {
        "field": "phone_number",
        "type": SheetFieldsTypes.PHONE.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "adresse - demandeur": {
        "field": "address",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "numéro de rue - demandeur": {
        "field": "address_number",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "rue - demandeur": {
        "field": "address_street",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "code postal - demandeur": {
        "field": "address_code",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "commune - demandeur": {
        "field": "address_location",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "complément - demandeur": {
        "field": "address_complement",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "type de demandeur": {
        "field": "type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "date de contact": {
        "field": "date_contact",
        "type": SheetFieldsTypes.DATE_DAY.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "provenance du contact": {
        "field": "contact_source",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "occupants majeurs": {
        "field": "adults_occupants_number",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "occupants mineurs": {
        "field": "minors_occupants_number",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "situation professionelle": {
        "field": "profession",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "catégorie de ressources": {
        "field": "resources_category",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "non éligible": {
        "field": "non_eligible",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "cause d'inéligibilité": {
        "field": "ineligibility",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "particulier": {
        "field": "is_private",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "nom de la société": {
        "field": "company_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "carte d'invalidité": {
        "field": "disability_card",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "taux": {
        "field": "rate_adaptation",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "bénéficiaire AAH": {
        "field": "has_AAH",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "bénéficiaire APA": {
        "field": "has_APA",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.REQUESTER.value,
    },
    "coefficient GIR": {
        "field": "GIR_coefficient",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.REQUESTER.value,
    },
}

taxable_income_fields_map = {
    "identifiant du rfr": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.TAXABLE_INCOME.value,
    },
    "identifiant du demandeur associé": {
        "field": "requester_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.TAXABLE_INCOME.value,
        "foreign_model": BaseEntities.REQUESTER.value,
        "key_in_foreign_table": "id",
    },
    "date": {
        "field": "date",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.TAXABLE_INCOME.value,
    },
    "RFR": {
        "field": "income",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.TAXABLE_INCOME.value,
    },
}

project_leads_fields_map = {
    "identifiant du référent": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.PROJECT_LEAD.value,
    },
    "identifiant du projet associé": {
        "field": "project_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.PROJECT_LEAD.value,
        "foreign_model": BaseEntities.PROJECT.value,
        "key_in_foreign_table": "id",
    },
    "adresse email du référent": {
        "field": "user_id",
        "type": SheetFieldsTypes.USER_EMAIL.value,
        "model": BaseEntities.PROJECT_LEAD.value,
    },
}

contacts_fields_map = {
    "identifiant du contact": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.CONTACT.value,
    },
    "identifiant du demandeur associé": {
        "field": "requester_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.CONTACT.value,
        "foreign_model": BaseEntities.REQUESTER.value,
        "key_in_foreign_table": "id",
    },
    "contact principal": {
        "field": "main_contact",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.CONTACT.value,
    },
    "email": {
        "field": "email",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "prenom": {
        "field": "first_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "nom": {
        "field": "last_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "adresse": {
        "field": "address",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "civilité": {
        "field": "title",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "commentaire": {
        "field": "comment",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.CONTACT.value,
    },
    "téléphone": {
        "field": "phone_number",
        "type": SheetFieldsTypes.PHONE.value,
        "model": BaseEntities.CONTACT.value,
    },
}


accommodations_fields_map = {
    "identifiant du logement": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "type de logement": {
        "field": "accommodation_type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "copropriété": {
        "field": "condominium",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "année d'acquisition": {
        "field": "purchase_year",
        "type": SheetFieldsTypes.DATE_YEAR.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "année de construction": {
        "field": "construction_year",
        "type": SheetFieldsTypes.DATE_YEAR.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nombre de niveaux": {
        "field": "levels_nb",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nombre de chambres": {
        "field": "rooms_nb",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "surface habitable": {
        "field": "living_area",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "surface additionnelle": {
        "field": "additional_area",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "vacant": {
        "field": "vacant",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nombre d'années vacant": {
        "field": "year_vacant_nb",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "commentaire": {
        "field": "commentary",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "identifiant du projet associé": {
        "field": "project_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.ACCOMMODATION.value,
        "foreign_model": BaseEntities.PROJECT.value,
        "key_in_foreign_table": "id",
    },
    "complément d'adresse": {
        "field": "address_complement",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nombre de locataires adultes": {
        "field": "adults_tenants_number",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nombre de locataires mineurs": {
        "field": "minors_tenants_number",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "montant loyer actuel": {
        "field": "current_rent",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "coefficient de dégradation": {
        "field": "degradation_coefficient",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "coefficient insalubrité": {
        "field": "unsanitary_coefficient",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nom du logement": {
        "field": "name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "logement hors projet": {
        "field": "out_of_project",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "montant loyer après travaux": {
        "field": "rent_after_renovation",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "commentaire du locataire": {
        "field": "tenant_commentary",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "email du locataire": {
        "field": "tenant_email",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "téléphone du locataire": {
        "field": "phone_number",
        "type": SheetFieldsTypes.PHONE.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "prénom du locataire": {
        "field": "tenant_first_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "nom du locataire": {
        "field": "tenant_last_name",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "civilité du locataire": {
        "field": "tenant_title",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "typologie": {
        "field": "typology",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "accès": {
        "field": "access",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "type de loyer après travaux": {
        "field": "type_rent_after_renovation",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "type de dossier": {
        "field": "case_type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "type de dossier secondaire": {
        "field": "secondary_case_type",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "coefficient GIR": {
        "field": "GIR_coefficient",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "carte handicapé": {
        "field": "disability_card",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "AAH": {
        "field": "has_AAH",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "APA": {
        "field": "has_APA",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    "taux d'adaptation": {
        "field": "rate_adaptation",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.ACCOMMODATION.value,
    },
}


common_areas_fields_map = {
    "identifiant de la partie commune": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "logement en copropriété": {
        "field": "condominium",
        "type": SheetFieldsTypes.BOOLEAN.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "année d'acquisition": {
        "field": "purchase_year",
        "type": SheetFieldsTypes.DATE_YEAR.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "année de construction": {
        "field": "construction_year",
        "type": SheetFieldsTypes.DATE_YEAR.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "nombre de niveaux": {
        "field": "levels_nb",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "commentaire": {
        "field": "commentary",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "nombre de logements": {
        "field": "accommodations_nb",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "identifiant du projet associé": {
        "field": "project_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.COMMON_AREA.value,
        "foreign_model": BaseEntities.PROJECT.value,
        "key_in_foreign_table": "id",
    },
    "surface habitable": {
        "field": "area",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "coefficient de dégradation": {
        "field": "degradation_coefficient",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "note": {
        "field": "note",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
    "coefficient insalubrité": {
        "field": "unsanitary_coefficient",
        "type": SheetFieldsTypes.FLOAT.value,
        "model": BaseEntities.COMMON_AREA.value,
    },
}


disorders_fields_map = {
    "identifiant du constats et recommandations": {
        "field": "id",
        "type": SheetFieldsTypes.PRIMARY_ID.value,
        "model": BaseEntities.DISORDER.value,
    },
    "priorité": {
        "field": "priority",
        "type": SheetFieldsTypes.INTEGER.value,
        "model": BaseEntities.DISORDER.value,
    },
    "identifiant du logement associé": {
        "field": "accommodation_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.DISORDER.value,
        "foreign_model": BaseEntities.ACCOMMODATION.value,
        "key_in_foreign_table": "id",
    },
    "identifiant de la partie commune associée": {
        "field": "common_area_id",
        "type": SheetFieldsTypes.FOREIGN_ID.value,
        "model": BaseEntities.DISORDER.value,
        "foreign_model": BaseEntities.COMMON_AREA.value,
        "key_in_foreign_table": "id",
    },
    "commentaire du constat": {
        "field": "analysis_comment",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.DISORDER.value,
    },
    "commentaire de la recommandation": {
        "field": "recommendation_comment",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.DISORDER.value,
    },
    "localisation du constat": {
        "field": "analysis_localisation",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.DISORDER.value,
    },
    "localisation de la recommandation": {
        "field": "recommendation_localisation",
        "type": SheetFieldsTypes.STRING.value,
        "model": BaseEntities.DISORDER.value,
    },
    "types de constat": {
        "type": SheetFieldsTypes.DISORDER_TYPE.value,
        "sub_type": SheetFieldsTypes.ANALYSIS.value,
        "model": BaseEntities.DISORDER.value,
    },
    "types de recommandation": {
        "type": SheetFieldsTypes.DISORDER_TYPE.value,
        "sub_type": SheetFieldsTypes.RECOMMMENDATION.value,
        "model": BaseEntities.DISORDER.value,
    },
}


# This SPREADSHEET_STRUCTURE is the key configuration dict that drives the projects importation.
# Contains information about data and labels positions.
# Each sheet comes with a "labels_fields_map" that link sheets labels and database entities fields.

SPREADSHEET_STRUCTURE = {
    SheetsList.REQUESTERS.value: {
        "labels_position": "B3:AE3",
        "data_position": "B5:AE",
        "labels_fields_map": requesters_fields_map,
        "model": BaseEntities.REQUESTER.value,
    },
    SheetsList.PROJECTS.value: {
        "labels_position": "B3:W5",
        "data_position": "B5:W",
        "labels_fields_map": projects_fields_map,
        "date_status_fields_map": date_status_fields_map,  # Need to associate status name to it's field name, then update project_fields_map
        "model": BaseEntities.PROJECT.value,
    },
    SheetsList.TAXABLE_INCOME.value: {
        "labels_position": "B3:E3",
        "data_position": "B5:E",
        "labels_fields_map": taxable_income_fields_map,
        "model": BaseEntities.TAXABLE_INCOME.value,
    },
    SheetsList.CONTACTS.value: {
        "labels_position": "B3:K3",
        "data_position": "B5:K",
        "labels_fields_map": contacts_fields_map,
        "model": BaseEntities.CONTACT.value,
    },
    SheetsList.PROJECTS_LEADS.value: {
        "labels_position": "B3:D3",
        "data_position": "B5:D",
        "labels_fields_map": project_leads_fields_map,
        "model": BaseEntities.PROJECT_LEAD.value,
    },
    SheetsList.ACCOMMODATIONS.value: {
        "labels_position": "B3:AK3",
        "data_position": "B5:AK",
        "labels_fields_map": accommodations_fields_map,
        "model": BaseEntities.ACCOMMODATION.value,
    },
    SheetsList.COMMON_AREA.value: {
        "labels_position": "B3:M3",
        "data_position": "B5:M",
        "labels_fields_map": common_areas_fields_map,
        "model": BaseEntities.COMMON_AREA.value,
    },
    SheetsList.DISORDERS.value: {
        "labels_position": "B3:K3",
        "data_position": "B5:K",
        "labels_fields_map": disorders_fields_map,
        "model": BaseEntities.DISORDER.value,
    },
}

INSTANTIATION_ORDER = {
    0: SheetsList.REQUESTERS.value,
    1: SheetsList.PROJECTS.value,
    2: SheetsList.TAXABLE_INCOME.value,
    3: SheetsList.CONTACTS.value,
    4: SheetsList.PROJECTS_LEADS.value,
    5: SheetsList.ACCOMMODATIONS.value,
    6: SheetsList.COMMON_AREA.value,
    7: SheetsList.DISORDERS.value,
}


class DataImportUtils:
    @staticmethod
    def fetch_data_from_sheet(sheet_id, user_email, A1_location):
        """From a given data sheet, fetch fields at the given A1 location"""
        sheet_file = SheetsUtils.get_spreadsheet_by_datafilter(
            sheet_id, A1_notation_filters=A1_location, user_email=user_email,
        )
        return SheetsUtils.format_sheet(sheet_file)

    @staticmethod
    def format_value(value, type):
        """Return formatted value, ready to be inserted into db"""
        if type in [SheetFieldsTypes.INTEGER.value, SheetFieldsTypes.DATE_YEAR.value]:
            value = int(value)
        elif type == SheetFieldsTypes.BOOLEAN.value:
            value = value == "OUI"
        elif type == SheetFieldsTypes.FLOAT.value:
            value = float(value)
        elif type == SheetFieldsTypes.DATE_DAY.value:
            try:
                value = datetime.datetime.strptime(value, FRENCH_DATE_FORMAT).date()
            except Exception as e:
                raise e

        return value

    # V2 Is there a better way to extract theses models ?
    @staticmethod
    def fetch_model(model_name):
        """From a given string, returns the corresponding SQL Alchemy Model"""
        from app.project import Requester
        from app.project.contacts import Contact
        from app.project.projects import Project
        from app.project.taxable_incomes import TaxableIncome
        from app.common.phone_number.model import PhoneNumber
        from app.project.accommodations.model import Accommodation
        from app.project.disorders.model import Disorder, DisorderType
        from app.project.common_areas.model import CommonArea
        from app.project.project_leads.model import ProjectLead
        from app.project.work_types.model import WorkType

        if model_name == BaseEntities.REQUESTER.value:
            return Requester
        elif model_name == BaseEntities.CONTACT.value:
            return Contact
        elif model_name == BaseEntities.PROJECT.value:
            return Project
        elif model_name == BaseEntities.TAXABLE_INCOME.value:
            return TaxableIncome
        elif model_name == BaseEntities.PHONE_NUMBER.value:
            return PhoneNumber
        elif model_name == BaseEntities.ACCOMMODATION.value:
            return Accommodation
        elif model_name == BaseEntities.DISORDER.value:
            return Disorder
        elif model_name == BaseEntities.DISORDER_TYPE.value:
            return DisorderType
        elif model_name == BaseEntities.COMMON_AREA.value:
            return CommonArea
        elif model_name == BaseEntities.PROJECT_LEAD.value:
            return ProjectLead
        if model_name == BaseEntities.WORK_TYPE.value:
            return WorkType

    @staticmethod
    def extract_phone_attrs(phone_number):
        """From raw phone value, extract phones fields and
        return a proper new_attr"""
        phone_values = phone_number.get("value").split("-")
        return {
            "country_code": phone_values[0].strip(),
            "international": phone_values[1].strip(),
            "national": phone_values[2].strip(),
            "resource_type": phone_values[3].strip(),
        }

    @staticmethod
    def extract_disorder_types_attrs(disorder_types):
        """From raw disorder_types value, extract disorder types fields and
        return a proper new_attr lists"""
        disorders_values = disorder_types.get("value").split("&")
        disorder_types_attrs_list = []
        for value in disorders_values:
            disorder_types_attrs_list.append(
                {
                    "type_name": value.strip(),
                    "is_analysis": disorder_types.get("sub_type")
                    == SheetFieldsTypes.ANALYSIS.value,
                }
            )
        return disorder_types_attrs_list

    @staticmethod
    def extract_work_types_attrs(work_types):
        """From raw work_types value, extract work_types fields and
        return a proper new_attr lists"""
        work_values = work_types.get("value").split("&")
        work_types_attrs_list = []
        for value in work_values:
            work_types_attrs_list.append(
                {"type_name": value.strip(),}
            )
        return work_types_attrs_list

    @staticmethod
    def fetch_user_id(mission_id, user_email_field):
        from app.auth.users.model import User
        import app.mission.permissions as missions_permissions

        """ From an email, fetch corresponding user from db, and return his id.
        If no active, and mission parametred user found with this ID, cancel workflow"""
        user_email = user_email_field.get("value").strip()
        user = (
            User.query.filter(User.email == user_email).filter(User.active == True)
        ).first()
        if not user:
            message = (
                f"No user found with the email address {user_email_field.get('value')}"
            )
            return message
        if user.role == UserRole.ADMIN:
            return user.id
        if not missions_permissions.MissionPermission.check_mission_permission(
            mission_id, user
        ):
            message = f"User identified with email address {user_email_field.get('value')} does not have access to the mission"
            return message
        return user.id
