"""Implémentation MongoDB du AlertRepository."""
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.alert import Alert, AlertLevel, AlertType
from src.domain.repositories.alert_repository import AlertRepository


class MongoAlertRepository(AlertRepository):
    COLLECTION = "alerts"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("lot_id")
        self._collection.create_index("resolved")
        self._collection.create_index([("resolved", 1), ("timestamp", -1)])

    def save(self, alert: Alert) -> Alert:
        data = alert.to_dict()
        data["timestamp"] = alert.timestamp
        result = self._collection.insert_one(data)
        alert.id = str(result.inserted_id)
        return alert

    def find_by_id(self, alert_id: str) -> Optional[Alert]:
        try:
            doc = self._collection.find_one({"_id": ObjectId(alert_id)})
        except Exception:
            return None
        return _to_entity(doc) if doc else None

    def find_by_lot(self, lot_id: str, limit: int = 100) -> list[Alert]:
        cursor = (
            self._collection
            .find({"lot_id": lot_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [_to_entity(doc) for doc in cursor]

    def find_active(self, limit: int = 100) -> list[Alert]:
        cursor = (
            self._collection
            .find({"resolved": False})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [_to_entity(doc) for doc in cursor]

    def mark_resolved(self, alert_id: str) -> bool:
        try:
            result = self._collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {"resolved": True, "resolved_at": datetime.now(timezone.utc)}},
            )
        except Exception:
            return False
        return result.modified_count > 0


def _to_entity(doc: dict) -> Alert:
    return Alert(
        id=str(doc["_id"]),
        lot_id=doc["lot_id"],
        alert_type=AlertType(doc["alert_type"]),
        level=AlertLevel(doc["level"]),
        message=doc["message"],
        value=float(doc["value"]),
        threshold=float(doc["threshold"]),
        timestamp=doc["timestamp"],
        resolved=bool(doc.get("resolved", False)),
    )
