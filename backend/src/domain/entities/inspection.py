"""Entité Inspection : rapport de vision par ordinateur (YOLO) sur un lot."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class InspectionClass(str, Enum):
    HEALTHY = "healthy"
    UNRIPE = "unripe"
    RIPE = "ripe"
    OVERRIPE = "overripe"
    MOLD = "mold"
    STAINED = "stained"
    UNKNOWN = "unknown"


class InspectionVerdict(str, Enum):
    OK = "ok"
    WARNING = "warning"
    REJECTED = "rejected"


@dataclass
class Detection:
    class_label: InspectionClass
    confidence: float
    bbox: list[float]  # [x1, y1, x2, y2] en pixels ou 0-1

    def to_dict(self) -> dict:
        return {
            "class_label": self.class_label.value,
            "confidence": self.confidence,
            "bbox": self.bbox,
        }


@dataclass
class Inspection:
    lot_code: str
    device_id: str
    detections: list[Detection]
    verdict: InspectionVerdict
    model_version: str
    image_path: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["verdict"] = self.verdict.value
        data["detections"] = [d.to_dict() for d in self.detections]
        if self.id is None:
            data.pop("id")
        return data
