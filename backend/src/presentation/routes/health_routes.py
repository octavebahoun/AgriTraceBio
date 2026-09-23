"""Route de santé pour vérifier l'état du serveur et de MongoDB."""
from flask import Blueprint, jsonify

from src.infrastructure.database.mongo_client import MongoConnection

health_bp = Blueprint("health", __name__, url_prefix="/api/health")


@health_bp.get("")
def health():
    mongo_ok = MongoConnection.ping()
    status = "ok" if mongo_ok else "degraded"
    code = 200 if mongo_ok else 503
    return jsonify({
        "status": status,
        "services": {"mongo": "up" if mongo_ok else "down"},
    }), code
