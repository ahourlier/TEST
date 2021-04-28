from datetime import date

from mypy_extensions import TypedDict


class AccommodationInterface(TypedDict, total=False):
    id: int
    accommodation_type: str
    condominium: bool
    purchase_year: date
    construction_year: date
    levels_nb: int
    rooms_nb: int
    living_area: float
    additional_area: float
    vacant: bool
    year_vacant_nb: int
    commentary: str
    project_id: int
    phone_number: dict
    name: str
    address_complement: str
    typology: str
    degradation_coefficient: float
    unsanitary_coefficient: float
    current_rent: float
    rent_after_renovation: float
    type_rent_after_renovation: str
    out_of_project: bool
    minors_tenants_number: int
    adults_tenants_number: int
    tenant_title: str
    tenant_last_name: str
    tenant_first_name: str
    tenant_email: str
    tenant_commentary: str
    access: str
    case_type: str
    secondary_case_type: str
    disability_card: bool
    rate_adaptation: int
    has_AAH: bool
    has_APA: bool
    GIR_coefficient: int
