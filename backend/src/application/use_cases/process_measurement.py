"""Use case orchestrateur : enregistre la mesure et génère les alertes."""
from dataclasses import dataclass

from src.domain.entities.alert import Alert
from src.domain.entities.block import EventType
from src.domain.entities.measurement import Measurement
from src.domain.repositories.alert_repository import AlertRepository
from src.domain.repositories.measurement_repository import MeasurementRepository
from src.domain.services.alert_detector import AlertDetector
from src.domain.services.blockchain_service import BlockchainService


@dataclass
class ProcessResult:
    measurement: Measurement
    alerts: list[Alert]


class ProcessMeasurementUseCase:
    def __init__(
        self,
        measurement_repo: MeasurementRepository,
        alert_repo: AlertRepository,
        detector: AlertDetector,
        blockchain: BlockchainService,
    ):
        self._measurement_repo = measurement_repo
        self._alert_repo = alert_repo
        self._detector = detector
        self._blockchain = blockchain

    def execute(
        self,
        lot_id: str,
        temperature: float,
        ethanol_ppm: float,
        air_quality_ppm: float,
        device_id: str,
    ) -> ProcessResult:
        measurement = Measurement(
            lot_id=lot_id,
            temperature=temperature,
            ethanol_ppm=ethanol_ppm,
            air_quality_ppm=air_quality_ppm,
            device_id=device_id,
        )
        saved = self._measurement_repo.save(measurement)

        detected = self._detector.detect(saved)
        saved_alerts = [self._alert_repo.save(a) for a in detected]

        for alert in saved_alerts:
            self._blockchain.append_event(
                EventType.ALERT_GENERATED,
                {
                    "alert_id": alert.id,
                    "alert_type": alert.alert_type.value,
                    "level": alert.level.value,
                    "value": alert.value,
                    "threshold": alert.threshold,
                },
                lot_code=alert.lot_id,
            )

        return ProcessResult(measurement=saved, alerts=saved_alerts)
