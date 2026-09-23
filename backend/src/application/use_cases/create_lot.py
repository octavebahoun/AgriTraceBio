"""Use case : créer un nouveau lot d'ananas."""
from datetime import datetime

from src.domain.entities.block import EventType
from src.domain.entities.lot import Lot, PineappleVariety
from src.domain.repositories.lot_repository import LotRepository
from src.domain.services.blockchain_service import BlockchainService


class CreateLotUseCase:
    def __init__(self, repository: LotRepository, blockchain: BlockchainService):
        self._repository = repository
        self._blockchain = blockchain

    def execute(
        self,
        lot_code: str,
        producer_name: str,
        variety: PineappleVariety,
        harvest_date: datetime,
        quantity_kg: float,
        origin_location: str,
        exporter_id: str,
        destination: str | None = None,
    ) -> Lot:
        lot = Lot(
            lot_code=lot_code,
            producer_name=producer_name,
            variety=variety,
            harvest_date=harvest_date,
            quantity_kg=quantity_kg,
            origin_location=origin_location,
            exporter_id=exporter_id,
            destination=destination,
        )
        saved = self._repository.save(lot)
        self._blockchain.append_event(
            EventType.LOT_CREATED,
            {
                "lot_id": saved.id,
                "producer_name": saved.producer_name,
                "variety": saved.variety.value,
                "quantity_kg": saved.quantity_kg,
                "origin_location": saved.origin_location,
                "exporter_id": saved.exporter_id,
                "harvest_date": saved.harvest_date.isoformat(),
            },
            lot_code=saved.lot_code,
        )
        return saved
