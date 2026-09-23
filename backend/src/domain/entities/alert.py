"""Entité Alert : anomalie détectée quand un seuil est dépassé."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, Enum):
    TEMPERATURE = "temperature"
    ETHANOL = "ethanol"
    AIR_QUALITY = "air_quality"


@dataclass
class Alert:
    lot_id: str
    alert_type: AlertType
    level: AlertLevel
    message: str
    value: float
    threshold: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["alert_type"] = self.alert_type.value
        data["level"] = self.level.value
        if self.id is None:
            data.pop("id")
        return data
