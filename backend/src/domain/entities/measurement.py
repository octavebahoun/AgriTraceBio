"""Entité Measurement : données IoT collectées par les capteurs du camion."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Measurement:
    lot_id: str
    temperature: float
    ethanol_ppm: float
    air_quality_ppm: float
    device_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        if self.id is None:
            data.pop("id")
        return data

    @staticmethod
    def from_dict(data: dict) -> "Measurement":
        return Measurement(
            id=str(data.get("_id")) if data.get("_id") else data.get("id"),
            lot_id=data["lot_id"],
            temperature=float(data["temperature"]),
            ethanol_ppm=float(data["ethanol_ppm"]),
            air_quality_ppm=float(data["air_quality_ppm"]),
            device_id=data["device_id"],
            timestamp=_parse_ts(data.get("timestamp")),
        )


def _parse_ts(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)
