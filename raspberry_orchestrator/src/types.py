"""Types partagés entre modules (sans dépendance ML)."""
from dataclasses import dataclass


@dataclass
class Detection:
    class_label: str
    confidence: float
    bbox: list[float]  # [x1, y1, x2, y2] en pixels
