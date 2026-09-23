"""Routes HTTP pour les lots d'ananas."""
from flask import Blueprint, jsonify, request

from src.domain.entities.user import UserRole
from src.infrastructure.repositories.mongo_lot_repository import (
    LotCodeAlreadyExists,
)
from src.presentation.middleware.auth_middleware import require_role
from src.presentation.routes.dependencies import (
    create_lot_uc,
    get_lot_by_code_uc,
    get_lot_by_id_uc,
    list_lots_uc,
    update_lot_status_uc,
)
from src.presentation.schemas.lot_schema import (
    LotInput,
    StatusInput,
    ValidationError,
)

lot_bp = Blueprint("lots", __name__, url_prefix="/api/lots")


@lot_bp.post("")
@require_role(UserRole.EXPORTER, UserRole.ADMIN)
def create_lot():
    try:
        payload = LotInput.from_json(request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400

    try:
        lot = create_lot_uc().execute(
            lot_code=payload.lot_code,
            producer_name=payload.producer_name,
            variety=payload.variety,
            harvest_date=payload.harvest_date,
            quantity_kg=payload.quantity_kg,
            origin_location=payload.origin_location,
            exporter_id=payload.exporter_id,
            destination=payload.destination,
        )
    except LotCodeAlreadyExists:
        return jsonify({"error": "lot_code_already_exists"}), 409
    return jsonify(lot.to_dict()), 201


@lot_bp.get("")
def list_lots():
    exporter_id = request.args.get("exporter_id")
    limit = min(int(request.args.get("limit", 100)), 500)
    lots = list_lots_uc().execute(exporter_id=exporter_id, limit=limit)
    return jsonify([lot.to_dict() for lot in lots])


@lot_bp.get("/<lot_id>")
def get_lot(lot_id: str):
    lot = get_lot_by_id_uc().execute(lot_id)
    if lot is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(lot.to_dict())


@lot_bp.get("/code/<lot_code>")
def get_lot_by_code(lot_code: str):
    lot = get_lot_by_code_uc().execute(lot_code)
    if lot is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(lot.to_dict())


@lot_bp.patch("/<lot_id>/status")
@require_role(UserRole.EXPORTER, UserRole.ADMIN)
def update_status(lot_id: str):
    try:
        payload = StatusInput.from_json(request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400
    lot = update_lot_status_uc().execute(lot_id, payload.status)
    if lot is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(lot.to_dict())
