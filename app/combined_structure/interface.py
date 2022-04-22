from typing import Optional
from datetime import date, datetime
from mypy_extensions import TypedDict


class CombinedStructureInterface(TypedDict):
    id: Optional[int]
    mission_id: Optional[int]
    mission: Optional[dict]
    # generalites
    name: Optional[str]
    type: Optional[str]
    currently_working_on: Optional[bool]
    nb_lots: Optional[int]
    nb_copros: Optional[int]
    creation_year: Optional[int]
    other_objects_linked: Optional[bool]
    other_objects_linked_details: Optional[str]
    # syndic et president
    president_id: Optional[int]
    president: Optional[dict]
    members_cs: Optional[str]
    # gestion fonctionnement
    main_member_exists: Optional[bool]
    main_member: Optional[str]
    # equipements contrats
    green_spaces: Optional[bool]
    heater: Optional[bool]
    aerial_parking: Optional[bool]
    underground_parking: Optional[bool]
    cctv: Optional[bool]
    other_equipments: Optional[bool]
    other_equipments_details: Optional[str]
    # contrats
    contract_syndic: Optional[bool]
    contract_syndic_date: Optional[str]
    contract_green_spaces: Optional[bool]
    contract_green_spaces_date: Optional[str]
    contract_heater: Optional[bool]
    contract_heater_date: Optional[str]
    contract_trash_room: Optional[bool]
    contract_trash_room_date: Optional[str]
    contract_trash_management: Optional[bool]
    contract_trash_management_date: Optional[str]
    contract_lodge: Optional[bool]
    contract_lodge_date: Optional[str]
    contract_aerial_parking: Optional[bool]
    contract_aerial_parking_date: Optional[str]
    contract_underground_parking: Optional[bool]
    contract_underground_parking_date: Optional[str]
    contract_cctv: Optional[bool]
    contract_cctv_date: Optional[str]
    other_technical_equipments: Optional[bool]
    # commentaires / precisions
    comment: Optional[str]
