"""Implémentation MongoDB du InspectionRepository."""
from typing import Optional
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.inspection import (
    Detection,
    Inspection,
    InspectionClass,
    InspectionVerdict,
)
from src.domain.repositories.inspection_repository import InspectionRepository


class MongoInspectionRepository(InspectionRepository):
    COLLECTION = "inspections"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("lot_code")
        self._collection.create_index([("lot_code", 1), ("timestamp", -1)])
        self._collection.create_index("verdict")

    def save(self, inspection: Inspection) -> Inspection:
        data = inspection.to_dict()
        data["timestamp"] = inspection.timestamp
        result = self._collection.insert_one(data)
        inspection.id = str(result.inserted_id)
        return inspection

    def find_by_id(self, inspection_id: str) -> Optional[Inspection]:
        try:
            doc = self._collection.find_one({"_id": ObjectId(inspection_id)})
        except Exception:
            return None
        return _to_entity(doc) if doc else None

    def find_by_lot(self, lot_code: str, limit: int = 100) -> list[Inspection]:
        cursor = (
            self._collection
            .find({"lot_code": lot_code})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [_to_entity(doc) for doc in cursor]

    def find_latest_by_lot(self, lot_code: str) -> Optional[Inspection]:
        doc = self._collection.find_one(
            {"lot_code": lot_code}, sort=[("timestamp", -1)]
        )
        return _to_entity(doc) if doc else None


def _to_entity(doc: dict) -> Inspection:
    return Inspection(
        id=str(doc["_id"]),
        lot_code=doc["lot_code"],
        device_id=doc["device_id"],
        detections=[
            Detection(
                class_label=InspectionClass(d["class_label"]),
                confidence=float(d["confidence"]),
                bbox=list(d["bbox"]),
            )
            for d in doc.get("detections", [])
        ],
        verdict=InspectionVerdict(doc["verdict"]),
        model_version=doc.get("model_version", "unknown"),
        image_path=doc.get("image_path"),
        timestamp=doc["timestamp"],
    )
