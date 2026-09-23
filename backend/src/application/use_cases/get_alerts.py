"""Use cases : lecture et résolution des alertes."""
from src.domain.entities.alert import Alert
from src.domain.repositories.alert_repository import AlertRepository


class GetAlertsByLotUseCase:
    def __init__(self, repository: AlertRepository):
        self._repository = repository

    def execute(self, lot_id: str, limit: int = 100) -> list[Alert]:
        return self._repository.find_by_lot(lot_id, limit)


class GetActiveAlertsUseCase:
    def __init__(self, repository: AlertRepository):
        self._repository = repository

    def execute(self, limit: int = 100) -> list[Alert]:
        return self._repository.find_active(limit)


class ResolveAlertUseCase:
    def __init__(self, repository: AlertRepository):
        self._repository = repository

    def execute(self, alert_id: str) -> bool:
        return self._repository.mark_resolved(alert_id)
