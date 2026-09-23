"""Routes HTTP pour les mesures IoT."""
from flask import Blueprint, jsonify, request

from src.presentation.routes.dependencies import (
    get_latest_measurement_uc,
    get_measurements_uc,
    process_measurement_uc,
)
from src.presentation.schemas.measurement_schema import (
    MeasurementInput,
    ValidationError,
)

measurement_bp = Blueprint("measurements", __name__, url_prefix="/api/measurements")


@measurement_bp.post("")
def create_measurement():
    try:
        payload = MeasurementInput.from_json(request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400

    result = process_measurement_uc().execute(
        lot_id=payload.lot_id,
        temperature=payload.temperature,
        ethanol_ppm=payload.ethanol_ppm,
        air_quality_ppm=payload.air_quality_ppm,
        device_id=payload.device_id,
    )
    return jsonify({
        "measurement": result.measurement.to_dict(),
        "alerts": [a.to_dict() for a in result.alerts],
    }), 201


@measurement_bp.get("/lot/<lot_id>")
def list_by_lot(lot_id: str):
    limit = min(int(request.args.get("limit", 100)), 500)
    measurements = get_measurements_uc().execute(lot_id, limit)
    return jsonify([m.to_dict() for m in measurements])


@measurement_bp.get("/lot/<lot_id>/latest")
def latest_by_lot(lot_id: str):
    measurement = get_latest_measurement_uc().execute(lot_id)
    if measurement is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(measurement.to_dict())
