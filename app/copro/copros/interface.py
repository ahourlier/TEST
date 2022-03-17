from typing import List, Optional
from datetime import date
from mypy_extensions import TypedDict


class CoproInterface(TypedDict, total=False):
    id: int
    mission_id: int
    # copropriété
    name: Optional[str]
    copro_type: Optional[str]
    address_1: Optional[dict]
    address_1_id: Optional[dict]
    address_2: Optional[dict]
    address_2_id: Optional[dict]
    user_in_charge_id: Optional[int]
    mixed_copro: Optional[bool]
    priority_copro: Optional[bool]
    horizontal_copro: Optional[bool]
    copro_registry_number: Optional[str]
    copro_creation_date: Optional[date]
    copro_creation_date: Optional[date]
    is_member_s1_s2: Optional[bool]
    is_member_association: Optional[bool]
    # Syndic
    syndic_name = Optional[str]
    syndic_type = Optional[str]
    syndic_contract_date = Optional[date]
    syndic_manager_name = Optional[str]
    syndic_manager_email = Optional[str]
    syndic_comment = Optional[str]
    syndic_manager_address_id = Optional[dict]
    syndic_manager_address = Optional[dict]
    syndic_manager_phone_number = Optional[dict]
    admin_name = Optional[str]
    admin_type = Optional[str]
    admin_contract_date = Optional[date]
    admin_manager_name = Optional[str]
    admin_manager_email = Optional[str]
    admin_comment = Optional[str]
    admin_manager_address_id = Optional[dict]
    admin_manager_address = Optional[dict]
    admin_manager_phone_number = Optional[dict]
    # Fonctionnement
    nb_lots: Optional[int]
    nb_co_owners: Optional[int]
    nb_sub_lots: Optional[int]
    percentage_lots_to_habitation: Optional[float]
    percentage_tantiemes_to_habitation: Optional[float]
    contract_end_date: Optional[date]
    closing_accounts_date: Optional[date]
    last_assembly_date: Optional[date]
    percentage_attending_tantiemes: Optional[float]
    percentage_attending_co_owners: Optional[float]
    institutional_landlords_presence: Optional[bool]
    # charges
    charges_last_year: Optional[float]
    provisional_budget_last_assembly: Optional[float]
    average_charges_per_quarter_per_lot: Optional[float]
    # description technique rapide
    construction_time: Optional[str]
    pmr: Optional[bool]
    igh: Optional[bool]
    external_spaces: Optional[bool]
    underground_parking: Optional[bool]
    aerial_parking: Optional[bool]
    cadastres: List[dict]
