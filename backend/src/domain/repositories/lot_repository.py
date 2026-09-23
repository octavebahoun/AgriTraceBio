"""Interface abstraite pour le repository des lots."""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.lot import Lot, LotStatus


class LotRepository(ABC):
    @abstractmethod
    def save(self, lot: Lot) -> Lot:
        ...

    @abstractmethod
    def find_by_id(self, lot_id: str) -> Optional[Lot]:
        ...

    @abstractmethod
    def find_by_code(self, lot_code: str) -> Optional[Lot]:
        ...

    @abstractmethod
    def find_by_exporter(self, exporter_id: str, limit: int = 100) -> list[Lot]:
        ...

    @abstractmethod
    def list_all(self, limit: int = 100) -> list[Lot]:
        ...

    @abstractmethod
    def update_status(self, lot_id: str, status: LotStatus) -> Optional[Lot]:
        ...
