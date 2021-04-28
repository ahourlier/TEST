import logging

PROJECT_ANONYMIZATION_MAP = {
    "address": None,
    "address_number": None,
    "address_street": None,
    "address_complement": None,
    "address_code": None,
    "address_latitude": None,
    "address_longitude": None,
}

REQUESTER_ANONYMIZATION_MAP = {
    "address": None,
    "address_number": None,
    "address_street": None,
    "address_complement": None,
    "address_code": None,
    "address_latitude": None,
    "address_longitude": None,
    "birthday_date": None,
    "email": None,
    "first_name": "champ anonymisé",
    "last_name": "champ anonymisé",
    "title": None,
}

ACCOMMODATION_ANONYMIZATION_MAP = {
    "tenant_email": None,
    "tenant_first_name": "champ anonymisé",
    "tenant_last_name": "champ anonymisé",
    "tenant_title": None,
}

CONTACT_ANONYMIZATION_MAP = {
    "address": "champ anonymisé",
    "email": None,
    "first_name": "champ anonymisé",
    "last_name": "champ anonymisé",
    "title": None,
}

PHONE_NUMBER_ANONYMIZATION_MAP = {
    "country_code": "FR",
    "international": " ",
    "kind": None,
    "national": " ",
}


class AnonymizationUtils:
    @staticmethod
    def anonymize_entity(entity, anonymization_map):
        if entity:
            for key, value in anonymization_map.items():
                setattr(entity, key, value)
        else:
            logging.error("Impossible to anonymize None entity")
