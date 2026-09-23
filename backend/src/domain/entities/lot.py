"""Entité Lot : un lot d'ananas de la récolte jusqu'à la livraison."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class LotStatus(str, Enum):
    CREATED = "created"
    IN_TRANSPORT = "in_transport"
    DELIVERED = "delivered"
    REJECTED = "rejected"


class PineappleVariety(str, Enum):
    CAYENNE_LISSE = "cayenne_lisse"
    PAIN_DE_SUCRE = "pain_de_sucre"


@dataclass
class Lot:
    lot_code: str
    producer_name: str
    variety: PineappleVariety
    harvest_date: datetime
    quantity_kg: float
    origin_location: str
    exporter_id: str
    destination: Optional[str] = None
    status: LotStatus = LotStatus.CREATED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["variety"] = self.variety.value
        data["status"] = self.status.value
        data["harvest_date"] = self.harvest_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        if self.id is None:
            data.pop("id")
        return data
