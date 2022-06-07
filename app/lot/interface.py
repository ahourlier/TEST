from datetime import date
from typing import Optional

from mypy_extensions import TypedDict


class LotInterface(TypedDict):

    id: Optional[int]

    copro_id: Optional[int]
    copro: Optional[dict]

    building_id: Optional[int]
    building: Optional[dict]
    # informations
    lot_number: Optional[int]
    client_number: Optional[str]
    type: Optional[str]
    owner_status: Optional[str]
    # tantieme et surface
    habitation_type: Optional[str]
    floor: Optional[str]
    door: Optional[str]
    surface: Optional[float]
    status_if_habitation: Optional[str]
    occupant_status: Optional[str]
    cave_surface: Optional[float]
    balcony_surface: Optional[float]
    # impayes
    unpaid_amount: Optional[float]
    unpaid_date: Optional[date]
    # Pour les logements loues, niveau de loyer
    lease_type: Optional[str]
    rent_hc_per_month: Optional[float]
    charges_per_month: Optional[float]
    rent_cc_per_month: Optional[float]
    intermediate_rent: Optional[bool]
    convention_rent_type: Optional[str]
    outstanding_payements_amount: Optional[float]
