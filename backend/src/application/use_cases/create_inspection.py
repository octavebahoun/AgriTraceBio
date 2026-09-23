"""Use case : enregistrer un rapport d'inspection YOLO + image."""
from dataclasses import dataclass
from typing import BinaryIO, Optional

from src.domain.entities.block import EventType
from src.domain.entities.inspection import Detection, Inspection
from src.domain.repositories.inspection_repository import InspectionRepository
from src.domain.services.blockchain_service import BlockchainService
from src.domain.services.image_storage import ImageStorage
from src.domain.services.verdict_calculator import VerdictCalculator


@dataclass
class InspectionInput:
    lot_code: str
    device_id: str
    detections: list[Detection]
    model_version: str
    image_stream: Optional[BinaryIO] = None
    image_extension: Optional[str] = None


class CreateInspectionUseCase:
    def __init__(
        self,
        repository: InspectionRepository,
        storage: ImageStorage,
        verdict_calc: VerdictCalculator,
        blockchain: BlockchainService,
    ):
        self._repository = repository
        self._storage = storage
        self._verdict_calc = verdict_calc
        self._blockchain = blockchain

    def execute(self, data: InspectionInput) -> Inspection:
        image_path = None
        if data.image_stream is not None and data.image_extension:
            image_path = self._storage.save(
                data.lot_code, data.image_stream, data.image_extension
            )

        inspection = Inspection(
            lot_code=data.lot_code,
            device_id=data.device_id,
            detections=data.detections,
            verdict=self._verdict_calc.compute(data.detections),
            model_version=data.model_version,
            image_path=image_path,
        )
        saved = self._repository.save(inspection)
        self._blockchain.append_event(
            EventType.INSPECTION_COMPLETED,
            {
                "inspection_id": saved.id,
                "verdict": saved.verdict.value,
                "model_version": saved.model_version,
                "detections_count": len(saved.detections),
                "image_path": saved.image_path,
            },
            lot_code=saved.lot_code,
        )
        return saved
