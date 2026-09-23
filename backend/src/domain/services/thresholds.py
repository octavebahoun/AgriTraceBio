"""Seuils critiques pour la conservation des ananas en transport."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Threshold:
    warning: float
    critical: float


TEMPERATURE_MIN = Threshold(warning=6.0, critical=4.0)
TEMPERATURE_MAX = Threshold(warning=10.0, critical=13.0)

ETHANOL_MAX = Threshold(warning=100.0, critical=200.0)

AIR_QUALITY_MAX = Threshold(warning=1000.0, critical=2000.0)
