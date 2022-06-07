from typing import Optional
from mypy_extensions import TypedDict


class CleRepartitionInterface(TypedDict):
    id: Optional[int]
    label: Optional[str]
    copro_id: Optional[int]


class CleRepartitionLotLinkInterface(TypedDict):
    id: Optional[int]
    lot_id: Optional[int]
    cle_repartition_id: Optional[int]
    tantieme: Optional[float]
