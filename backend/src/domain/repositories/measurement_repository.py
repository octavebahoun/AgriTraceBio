"""Interface abstraite pour le repository des mesures."""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.measurement import Measurement


class MeasurementRepository(ABC):
    @abstractmethod
    def save(self, measurement: Measurement) -> Measurement:
        ...

    @abstractmethod
    def find_by_id(self, measurement_id: str) -> Optional[Measurement]:
        ...

    @abstractmethod
    def find_by_lot(self, lot_id: str, limit: int = 100) -> list[Measurement]:
        ...

    @abstractmethod
    def find_latest_by_lot(self, lot_id: str) -> Optional[Measurement]:
        ...
