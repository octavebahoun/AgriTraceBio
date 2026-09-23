"""Use case : produire un certificat PDF de traçabilité pour un lot."""
from dataclasses import dataclass
from typing import Optional

from src.domain.repositories.alert_repository import AlertRepository
from src.domain.repositories.blockchain_repository import BlockchainRepository
from src.domain.repositories.inspection_repository import InspectionRepository
from src.domain.repositories.lot_repository import LotRepository
from src.domain.repositories.measurement_repository import MeasurementRepository
from src.domain.services.certificate_generator import (
    CertificateGenerator,
    CertificateInput,
)
from src.domain.services.qr_generator import QrGenerator


@dataclass
class CertificateResult:
    lot_code: str
    pdf_bytes: bytes


class GenerateCertificateUseCase:
    def __init__(
        self,
        lot_repo: LotRepository,
        measurement_repo: MeasurementRepository,
        alert_repo: AlertRepository,
        inspection_repo: InspectionRepository,
        blockchain_repo: BlockchainRepository,
        qr_generator: QrGenerator,
        pdf_generator: CertificateGenerator,
    ):
        self._lot_repo = lot_repo
        self._measurement_repo = measurement_repo
        self._alert_repo = alert_repo
        self._inspection_repo = inspection_repo
        self._blockchain_repo = blockchain_repo
        self._qr = qr_generator
        self._pdf = pdf_generator

    def execute(self, lot_code: str) -> Optional[CertificateResult]:
        lot = self._lot_repo.find_by_code(lot_code)
        if lot is None:
            return None

        data = CertificateInput(
            lot=lot,
            measurements=self._measurement_repo.find_by_lot(lot.lot_code, 100),
            alerts=self._alert_repo.find_by_lot(lot.lot_code, 100),
            inspections=self._inspection_repo.find_by_lot(lot.lot_code, 100),
            blockchain=self._blockchain_repo.find_by_lot(lot.lot_code, 500),
            trace_url=self._qr.build_trace_url(lot.lot_code),
        )
        return CertificateResult(
            lot_code=lot.lot_code,
            pdf_bytes=self._pdf.generate(data),
        )
