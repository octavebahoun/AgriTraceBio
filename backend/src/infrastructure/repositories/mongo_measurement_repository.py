"""Implémentation MongoDB du MeasurementRepository."""
from typing import Optional
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.measurement import Measurement
from src.domain.repositories.measurement_repository import MeasurementRepository


class MongoMeasurementRepository(MeasurementRepository):
    COLLECTION = "measurements"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("lot_id")
        self._collection.create_index([("lot_id", 1), ("timestamp", -1)])

    def save(self, measurement: Measurement) -> Measurement:
        data = measurement.to_dict()
        data["timestamp"] = measurement.timestamp
        result = self._collection.insert_one(data)
        measurement.id = str(result.inserted_id)
        return measurement

    def find_by_id(self, measurement_id: str) -> Optional[Measurement]:
        try:
            doc = self._collection.find_one({"_id": ObjectId(measurement_id)})
        except Exception:
            return None
        return Measurement.from_dict(doc) if doc else None

    def find_by_lot(self, lot_id: str, limit: int = 100) -> list[Measurement]:
        cursor = (
            self._collection
            .find({"lot_id": lot_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [Measurement.from_dict(doc) for doc in cursor]

    def find_latest_by_lot(self, lot_id: str) -> Optional[Measurement]:
        doc = self._collection.find_one(
            {"lot_id": lot_id},
            sort=[("timestamp", -1)],
        )
        return Measurement.from_dict(doc) if doc else None
