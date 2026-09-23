"""Use case : dossier de traçabilité public d'un lot (via QR code)."""
from dataclasses import dataclass
from typing import Optional

from src.domain.entities.alert import Alert
from src.domain.entities.inspection import Inspection
from src.domain.entities.lot import Lot
from src.domain.entities.measurement import Measurement
from src.domain.repositories.alert_repository import AlertRepository
from src.domain.repositories.inspection_repository import InspectionRepository
from src.domain.repositories.lot_repository import LotRepository
from src.domain.repositories.measurement_repository import MeasurementRepository


@dataclass
class LotTrace:
    lot: Lot
    measurements: list[Measurement]
    alerts: list[Alert]
    inspections: list[Inspection]


class GetLotTraceUseCase:
    def __init__(
        self,
        lot_repo: LotRepository,
        measurement_repo: MeasurementRepository,
        alert_repo: AlertRepository,
        inspection_repo: InspectionRepository,
    ):
        self._lot_repo = lot_repo
        self._measurement_repo = measurement_repo
        self._alert_repo = alert_repo
        self._inspection_repo = inspection_repo

    def execute(self, lot_code: str, history_limit: int = 200) -> Optional[LotTrace]:
        lot = self._lot_repo.find_by_code(lot_code)
        if lot is None:
            return None
        return LotTrace(
            lot=lot,
            measurements=self._measurement_repo.find_by_lot(lot.lot_code, history_limit),
            alerts=self._alert_repo.find_by_lot(lot.lot_code, history_limit),
            inspections=self._inspection_repo.find_by_lot(lot.lot_code, history_limit),
        )
