"""Use case : générer le QR code SVG d'un lot existant."""
from dataclasses import dataclass
from typing import Optional

from src.domain.repositories.lot_repository import LotRepository
from src.domain.services.qr_generator import QrGenerator


@dataclass
class QrResult:
    lot_code: str
    trace_url: str
    svg: bytes


class GenerateQrCodeUseCase:
    def __init__(self, lot_repo: LotRepository, generator: QrGenerator):
        self._lot_repo = lot_repo
        self._generator = generator

    def execute(self, lot_code: str) -> Optional[QrResult]:
        lot = self._lot_repo.find_by_code(lot_code)
        if lot is None:
            return None
        return QrResult(
            lot_code=lot.lot_code,
            trace_url=self._generator.build_trace_url(lot.lot_code),
            svg=self._generator.generate_svg(lot.lot_code),
        )
