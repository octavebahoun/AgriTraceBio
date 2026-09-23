"""Interface abstraite pour le repository des alertes."""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.alert import Alert


class AlertRepository(ABC):
    @abstractmethod
    def save(self, alert: Alert) -> Alert:
        ...

    @abstractmethod
    def find_by_id(self, alert_id: str) -> Optional[Alert]:
        ...

    @abstractmethod
    def find_by_lot(self, lot_id: str, limit: int = 100) -> list[Alert]:
        ...

    @abstractmethod
    def find_active(self, limit: int = 100) -> list[Alert]:
        ...

    @abstractmethod
    def mark_resolved(self, alert_id: str) -> bool:
        ...
