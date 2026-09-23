"""Validation manuelle des entrées HTTP pour les mesures."""
from dataclasses import dataclass


class ValidationError(Exception):
    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__(str(errors))


@dataclass
class MeasurementInput:
    lot_id: str
    temperature: float
    ethanol_ppm: float
    air_quality_ppm: float
    device_id: str

    @staticmethod
    def from_json(data: dict | None) -> "MeasurementInput":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])

        lot_id = _str(data, "lot_id", errors, 1, 100)
        device_id = _str(data, "device_id", errors, 1, 100)
        temperature = _num(data, "temperature", errors, -40.0, 100.0)
        ethanol_ppm = _num(data, "ethanol_ppm", errors, 0.0, None)
        air_quality_ppm = _num(data, "air_quality_ppm", errors, 0.0, None)

        if errors:
            raise ValidationError(errors)
        return MeasurementInput(lot_id, temperature, ethanol_ppm,
                                air_quality_ppm, device_id)


def _str(data, key, errors, mn, mx):
    v = data.get(key)
    if not isinstance(v, str) or not (mn <= len(v) <= mx):
        errors.append({"field": key, "msg": f"string {mn}-{mx} chars required"})
        return ""
    return v


def _num(data, key, errors, mn, mx):
    v = data.get(key)
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        errors.append({"field": key, "msg": "number required"})
        return 0.0
    if mn is not None and v < mn:
        errors.append({"field": key, "msg": f">= {mn} required"})
    if mx is not None and v > mx:
        errors.append({"field": key, "msg": f"<= {mx} required"})
    return float(v)
