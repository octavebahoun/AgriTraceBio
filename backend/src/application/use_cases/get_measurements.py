"""Use cases : lecture des mesures."""
from typing import Optional

from src.domain.entities.measurement import Measurement
from src.domain.repositories.measurement_repository import MeasurementRepository


class GetMeasurementsByLotUseCase:
    def __init__(self, repository: MeasurementRepository):
        self._repository = repository

    def execute(self, lot_id: str, limit: int = 100) -> list[Measurement]:
        return self._repository.find_by_lot(lot_id, limit)


class GetLatestMeasurementUseCase:
    def __init__(self, repository: MeasurementRepository):
        self._repository = repository

    def execute(self, lot_id: str) -> Optional[Measurement]:
        return self._repository.find_latest_by_lot(lot_id)
