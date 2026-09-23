"""Use cases : lecture des inspections."""
from typing import Optional

from src.domain.entities.inspection import Inspection
from src.domain.repositories.inspection_repository import InspectionRepository


class GetInspectionsByLotUseCase:
    def __init__(self, repository: InspectionRepository):
        self._repository = repository

    def execute(self, lot_code: str, limit: int = 100) -> list[Inspection]:
        return self._repository.find_by_lot(lot_code, limit)


class GetLatestInspectionUseCase:
    def __init__(self, repository: InspectionRepository):
        self._repository = repository

    def execute(self, lot_code: str) -> Optional[Inspection]:
        return self._repository.find_latest_by_lot(lot_code)


class GetInspectionByIdUseCase:
    def __init__(self, repository: InspectionRepository):
        self._repository = repository

    def execute(self, inspection_id: str) -> Optional[Inspection]:
        return self._repository.find_by_id(inspection_id)
