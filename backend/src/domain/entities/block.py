"""Entité Block : maillon d'une chaîne d'événements infalsifiable."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    LOT_CREATED = "lot_created"
    LOT_STATUS_CHANGED = "lot_status_changed"
    ALERT_GENERATED = "alert_generated"
    INSPECTION_COMPLETED = "inspection_completed"


GENESIS_HASH = "0" * 64


def _now_ms() -> datetime:
    """Retourne l'heure UTC arrondie à la milliseconde (précision BSON)."""
    now = datetime.now(timezone.utc)
    return now.replace(microsecond=(now.microsecond // 1000) * 1000)


@dataclass
class Block:
    index: int
    previous_hash: str
    event_type: EventType
    event_data: dict
    lot_code: Optional[str] = None
    timestamp: datetime = field(default_factory=_now_ms)
    hash: str = ""
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["event_type"] = self.event_type.value
        if self.id is None:
            data.pop("id")
        return data
