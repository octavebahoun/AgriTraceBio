"""Interface abstraite pour le repository des inspections."""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.inspection import Inspection


class InspectionRepository(ABC):
    @abstractmethod
    def save(self, inspection: Inspection) -> Inspection:
        ...

    @abstractmethod
    def find_by_id(self, inspection_id: str) -> Optional[Inspection]:
        ...

    @abstractmethod
    def find_by_lot(self, lot_code: str, limit: int = 100) -> list[Inspection]:
        ...

    @abstractmethod
    def find_latest_by_lot(self, lot_code: str) -> Optional[Inspection]:
        ...
