"""Use case : enregistrer une nouvelle mesure IoT."""
from src.domain.entities.measurement import Measurement
from src.domain.repositories.measurement_repository import MeasurementRepository


class CreateMeasurementUseCase:
    def __init__(self, repository: MeasurementRepository):
        self._repository = repository

    def execute(
        self,
        lot_id: str,
        temperature: float,
        ethanol_ppm: float,
        air_quality_ppm: float,
        device_id: str,
    ) -> Measurement:
        measurement = Measurement(
            lot_id=lot_id,
            temperature=temperature,
            ethanol_ppm=ethanol_ppm,
            air_quality_ppm=air_quality_ppm,
            device_id=device_id,
        )
        return self._repository.save(measurement)
