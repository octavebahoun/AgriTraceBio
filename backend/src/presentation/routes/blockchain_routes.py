"""Routes HTTP pour consulter et vérifier la blockchain."""
from dataclasses import asdict

from flask import Blueprint, jsonify, request

from src.presentation.routes.dependencies import (
    get_blockchain_by_lot_uc,
    list_blockchain_uc,
    verify_blockchain_uc,
)

blockchain_bp = Blueprint("blockchain", __name__, url_prefix="/api/blockchain")


@blockchain_bp.get("")
def list_blocks():
    limit = min(int(request.args.get("limit", 100)), 500)
    blocks = list_blockchain_uc().execute(limit)
    return jsonify([b.to_dict() for b in blocks])


@blockchain_bp.get("/lot/<lot_code>")
def blocks_by_lot(lot_code: str):
    limit = min(int(request.args.get("limit", 500)), 500)
    blocks = get_blockchain_by_lot_uc().execute(lot_code, limit)
    return jsonify([b.to_dict() for b in blocks])


@blockchain_bp.get("/verify")
def verify():
    result = verify_blockchain_uc().execute()
    payload = asdict(result)
    return jsonify(payload), 200 if result.valid else 409
