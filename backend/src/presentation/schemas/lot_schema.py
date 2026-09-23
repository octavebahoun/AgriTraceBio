"""Validation manuelle des entrées HTTP pour les lots."""
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.lot import LotStatus, PineappleVariety
from src.presentation.schemas.measurement_schema import (
    ValidationError,
    _num,
    _str,
)


@dataclass
class LotInput:
    lot_code: str
    producer_name: str
    variety: PineappleVariety
    harvest_date: datetime
    quantity_kg: float
    origin_location: str
    exporter_id: str
    destination: str | None

    @staticmethod
    def from_json(data: dict | None) -> "LotInput":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])

        lot_code = _str(data, "lot_code", errors, 1, 50)
        producer_name = _str(data, "producer_name", errors, 1, 200)
        origin_location = _str(data, "origin_location", errors, 1, 200)
        exporter_id = _str(data, "exporter_id", errors, 1, 100)
        quantity_kg = _num(data, "quantity_kg", errors, 0.1, 100000.0)
        variety = _enum(data, "variety", PineappleVariety, errors)
        harvest_date = _date(data, "harvest_date", errors)
        destination = data.get("destination") if isinstance(
            data.get("destination"), str) else None

        if errors:
            raise ValidationError(errors)
        return LotInput(lot_code, producer_name, variety, harvest_date,
                        quantity_kg, origin_location, exporter_id, destination)


@dataclass
class StatusInput:
    status: LotStatus

    @staticmethod
    def from_json(data: dict | None) -> "StatusInput":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])
        status = _enum(data, "status", LotStatus, errors)
        if errors:
            raise ValidationError(errors)
        return StatusInput(status)


def _enum(data, key, enum_cls, errors):
    v = data.get(key)
    if not isinstance(v, str):
        errors.append({"field": key, "msg": "string required"})
        return next(iter(enum_cls))
    try:
        return enum_cls(v)
    except ValueError:
        allowed = [e.value for e in enum_cls]
        errors.append({"field": key, "msg": f"must be one of {allowed}"})
        return next(iter(enum_cls))


def _date(data, key, errors) -> datetime:
    v = data.get(key)
    if not isinstance(v, str):
        errors.append({"field": key, "msg": "ISO datetime string required"})
        return datetime.now()
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        errors.append({"field": key, "msg": "invalid ISO datetime"})
        return datetime.now()
