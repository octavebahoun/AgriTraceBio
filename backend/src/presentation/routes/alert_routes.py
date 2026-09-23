"""Routes HTTP pour les alertes."""
from flask import Blueprint, jsonify, request

from src.domain.entities.user import UserRole
from src.presentation.middleware.auth_middleware import require_role
from src.presentation.routes.dependencies import (
    get_active_alerts_uc,
    get_alerts_by_lot_uc,
    resolve_alert_uc,
)

alert_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")


@alert_bp.get("/lot/<lot_id>")
def list_by_lot(lot_id: str):
    limit = min(int(request.args.get("limit", 100)), 500)
    alerts = get_alerts_by_lot_uc().execute(lot_id, limit)
    return jsonify([a.to_dict() for a in alerts])


@alert_bp.get("/active")
def list_active():
    limit = min(int(request.args.get("limit", 100)), 500)
    alerts = get_active_alerts_uc().execute(limit)
    return jsonify([a.to_dict() for a in alerts])


@alert_bp.post("/<alert_id>/resolve")
@require_role(UserRole.CONTROLLER, UserRole.EXPORTER, UserRole.ADMIN)
def resolve(alert_id: str):
    ok = resolve_alert_uc().execute(alert_id)
    if not ok:
        return jsonify({"error": "not_found"}), 404
    return jsonify({"status": "resolved", "id": alert_id})
