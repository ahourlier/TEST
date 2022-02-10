from datetime import date

from mypy_extensions import TypedDict


class RequesterInterface(TypedDict, total=False):
    id: int
    email: str
    last_name: str
    first_name: str
    title: str
    birthday_date: date
    phone_number_1: dict
    phone_number_2: dict
    type: str
    address: str
    cadastral_reference: str
    date_contact: date
    contact_source: str
    minors_occupants_number: int
    adults_occupants_number: int
    profession: str
    resources_category: str
    non_eligible: bool
    ineligibility: str
    PTZ_year: date
    is_private: bool
    company_name: str
    disability_card: bool
    rate_adaptation: int
    has_AAH: bool
    has_APA: bool
    GIR_coefficient: int
