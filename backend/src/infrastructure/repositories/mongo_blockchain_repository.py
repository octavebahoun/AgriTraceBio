"""Implémentation MongoDB du BlockchainRepository."""
from typing import Iterator, Optional
from pymongo.database import Database

from src.domain.entities.block import Block, EventType
from src.domain.repositories.blockchain_repository import BlockchainRepository


class MongoBlockchainRepository(BlockchainRepository):
    COLLECTION = "blockchain"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("index", unique=True)
        self._collection.create_index("lot_code")

    def append(self, block: Block) -> Block:
        data = block.to_dict()
        data["timestamp"] = block.timestamp
        result = self._collection.insert_one(data)
        block.id = str(result.inserted_id)
        return block

    def get_last(self) -> Optional[Block]:
        doc = self._collection.find_one(sort=[("index", -1)])
        return _to_entity(doc) if doc else None

    def list_all(self, limit: int = 500) -> list[Block]:
        cursor = self._collection.find().sort("index", -1).limit(limit)
        return [_to_entity(doc) for doc in cursor]

    def find_by_lot(self, lot_code: str, limit: int = 500) -> list[Block]:
        cursor = (
            self._collection
            .find({"lot_code": lot_code})
            .sort("index", 1)
            .limit(limit)
        )
        return [_to_entity(doc) for doc in cursor]

    def iter_ordered(self) -> Iterator[Block]:
        for doc in self._collection.find().sort("index", 1):
            yield _to_entity(doc)


def _to_entity(doc: dict) -> Block:
    return Block(
        id=str(doc["_id"]),
        index=int(doc["index"]),
        previous_hash=doc["previous_hash"],
        event_type=EventType(doc["event_type"]),
        event_data=dict(doc.get("event_data", {})),
        lot_code=doc.get("lot_code"),
        timestamp=doc["timestamp"],
        hash=doc["hash"],
    )
