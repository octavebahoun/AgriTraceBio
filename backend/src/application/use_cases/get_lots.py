"""Use cases : lecture et mise à jour des lots."""
from typing import Optional

from src.domain.entities.block import EventType
from src.domain.entities.lot import Lot, LotStatus
from src.domain.repositories.lot_repository import LotRepository
from src.domain.services.blockchain_service import BlockchainService


class GetLotByIdUseCase:
    def __init__(self, repository: LotRepository):
        self._repository = repository

    def execute(self, lot_id: str) -> Optional[Lot]:
        return self._repository.find_by_id(lot_id)


class GetLotByCodeUseCase:
    def __init__(self, repository: LotRepository):
        self._repository = repository

    def execute(self, lot_code: str) -> Optional[Lot]:
        return self._repository.find_by_code(lot_code)


class ListLotsUseCase:
    def __init__(self, repository: LotRepository):
        self._repository = repository

    def execute(self, exporter_id: Optional[str] = None,
                limit: int = 100) -> list[Lot]:
        if exporter_id:
            return self._repository.find_by_exporter(exporter_id, limit)
        return self._repository.list_all(limit)


class UpdateLotStatusUseCase:
    def __init__(self, repository: LotRepository, blockchain: BlockchainService):
        self._repository = repository
        self._blockchain = blockchain

    def execute(self, lot_id: str, status: LotStatus) -> Optional[Lot]:
        lot = self._repository.update_status(lot_id, status)
        if lot is not None:
            self._blockchain.append_event(
                EventType.LOT_STATUS_CHANGED,
                {"lot_id": lot.id, "new_status": status.value},
                lot_code=lot.lot_code,
            )
        return lot
