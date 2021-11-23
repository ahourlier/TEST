from typing import Optional
from datetime import date
from mypy_extensions import TypedDict


class BuildingInterface(TypedDict):
    id: Optional[int]
    copro_id: Optional[int]
    # batiment
    name: Optional[str]
    address_id: Optional[int]
    address: Optional[dict]
    # contact
    referents: Optional[str]
    # generalites du batiment
    construction_time: Optional[str]
    igh: Optional[bool]
    r_plus: Optional[str]
    r_minus: Optional[str]
    erp: Optional[bool]
    erp_category: Optional[str]
    last_security_commission_date: Optional[date]
    lodge: Optional[bool]
    nb_habitations_rcp: Optional[int]
    nb_habitations_noted: Optional[int]
    total_surface: Optional[float]
    nb_annex_lots: Optional[int]
    nb_aerial_parking_spaces: Optional[int]
    nb_underground_parking_spaces: Optional[int]
    # acces
    access_type: Optional[str]
    access_code: Optional[str]
    access_type_cave: Optional[str]
    access_type_roof: Optional[str]
    # caracteristiques techniques
    lifts: Optional[int]
    roof: Optional[str]
    vmc: Optional[bool]
    collective_heater: Optional[str]
    ground_heating: Optional[bool]
    individual_cold_water_counter: Optional[bool]
    individual_ecs_counter: Optional[bool]
    other_equipments: Optional[str]
    # diagnostique technique
    energy_diagnosis_date: Optional[date]
    initial_energy_label: Optional[str]
    initial_consumption: Optional[float]
    asbestos_diagnosis_date: Optional[date]
    asbestos_diagnosis_result: Optional[str]
    lead_diagnosis_date: Optional[date]
    security_commission_date: Optional[date]
    security_commission_result: Optional[str]
    other_technical_diagnosis: Optional[str]
    # commentaires / precisions
    comment: Optional[str]
