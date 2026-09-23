"""Implémentation MongoDB du LotRepository."""
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from src.domain.entities.lot import Lot, LotStatus, PineappleVariety
from src.domain.repositories.lot_repository import LotRepository


class LotCodeAlreadyExists(Exception):
    pass


class MongoLotRepository(LotRepository):
    COLLECTION = "lots"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("lot_code", unique=True)
        self._collection.create_index("exporter_id")
        self._collection.create_index("status")

    def save(self, lot: Lot) -> Lot:
        data = lot.to_dict()
        data["harvest_date"] = lot.harvest_date
        data["created_at"] = lot.created_at
        data["updated_at"] = lot.updated_at
        try:
            result = self._collection.insert_one(data)
        except DuplicateKeyError:
            raise LotCodeAlreadyExists(lot.lot_code)
        lot.id = str(result.inserted_id)
        return lot

    def find_by_id(self, lot_id: str) -> Optional[Lot]:
        try:
            doc = self._collection.find_one({"_id": ObjectId(lot_id)})
        except Exception:
            return None
        return _to_entity(doc) if doc else None

    def find_by_code(self, lot_code: str) -> Optional[Lot]:
        doc = self._collection.find_one({"lot_code": lot_code})
        return _to_entity(doc) if doc else None

    def find_by_exporter(self, exporter_id: str, limit: int = 100) -> list[Lot]:
        cursor = (
            self._collection
            .find({"exporter_id": exporter_id})
            .sort("created_at", -1)
            .limit(limit)
        )
        return [_to_entity(doc) for doc in cursor]

    def list_all(self, limit: int = 100) -> list[Lot]:
        cursor = self._collection.find().sort("created_at", -1).limit(limit)
        return [_to_entity(doc) for doc in cursor]

    def update_status(self, lot_id: str, status: LotStatus) -> Optional[Lot]:
        try:
            doc = self._collection.find_one_and_update(
                {"_id": ObjectId(lot_id)},
                {"$set": {
                    "status": status.value,
                    "updated_at": datetime.now(timezone.utc),
                }},
                return_document=True,
            )
        except Exception:
            return None
        return _to_entity(doc) if doc else None


def _to_entity(doc: dict) -> Lot:
    return Lot(
        id=str(doc["_id"]),
        lot_code=doc["lot_code"],
        producer_name=doc["producer_name"],
        variety=PineappleVariety(doc["variety"]),
        harvest_date=doc["harvest_date"],
        quantity_kg=float(doc["quantity_kg"]),
        origin_location=doc["origin_location"],
        exporter_id=doc["exporter_id"],
        destination=doc.get("destination"),
        status=LotStatus(doc.get("status", "created")),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )
