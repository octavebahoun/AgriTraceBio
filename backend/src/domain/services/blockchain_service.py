"""Service : chaînage SHA-256, append d'événement, vérification d'intégrité."""
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from src.domain.entities.block import GENESIS_HASH, Block, EventType
from src.domain.repositories.blockchain_repository import BlockchainRepository


@dataclass
class VerifyResult:
    valid: bool
    total_blocks: int
    broken_at_index: Optional[int] = None
    reason: Optional[str] = None


class BlockchainService:
    def __init__(self, repository: BlockchainRepository):
        self._repository = repository

    def append_event(
        self,
        event_type: EventType,
        event_data: dict,
        lot_code: Optional[str] = None,
    ) -> Block:
        last = self._repository.get_last()
        prev_hash = last.hash if last else GENESIS_HASH
        index = (last.index + 1) if last else 0

        block = Block(
            index=index,
            previous_hash=prev_hash,
            event_type=event_type,
            event_data=event_data,
            lot_code=lot_code,
        )
        block.hash = self._compute_hash(block)
        return self._repository.append(block)

    def verify_chain(self) -> VerifyResult:
        count = 0
        expected_prev = GENESIS_HASH
        expected_index = 0
        for block in self._repository.iter_ordered():
            if block.index != expected_index:
                return VerifyResult(False, count, block.index,
                                    f"index mismatch (expected {expected_index})")
            if block.previous_hash != expected_prev:
                return VerifyResult(False, count, block.index,
                                    "previous_hash mismatch")
            recomputed = self._compute_hash(block)
            if recomputed != block.hash:
                return VerifyResult(False, count, block.index,
                                    "hash mismatch (tampered content)")
            expected_prev = block.hash
            expected_index += 1
            count += 1
        return VerifyResult(True, count)

    def _compute_hash(self, block: Block) -> str:
        payload = {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "event_type": block.event_type.value,
            "event_data": block.event_data,
            "lot_code": block.lot_code,
            "timestamp": _canonical_ts(block.timestamp),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         default=str).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


def _canonical_ts(ts: datetime) -> str:
    """Timestamp UTC arrondi ms, avec suffixe fixe (survit au round-trip BSON)."""
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    else:
        ts = ts.astimezone(timezone.utc)
    ts = ts.replace(microsecond=(ts.microsecond // 1000) * 1000)
    return ts.isoformat()
