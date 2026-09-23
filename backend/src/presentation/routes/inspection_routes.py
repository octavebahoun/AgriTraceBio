"""Routes HTTP pour les inspections YOLO."""
import os

from flask import Blueprint, jsonify, request, send_file

from src.application.use_cases.create_inspection import InspectionInput
from src.domain.entities.user import UserRole
from src.presentation.middleware.auth_middleware import require_role
from src.presentation.routes.dependencies import (
    create_inspection_uc,
    get_inspection_by_id_uc,
    get_inspections_by_lot_uc,
    get_latest_inspection_uc,
    image_storage,
)
from src.presentation.schemas.inspection_schema import (
    InspectionPayload,
    ValidationError,
)

inspection_bp = Blueprint("inspections", __name__, url_prefix="/api/inspections")


@inspection_bp.post("")
def create_inspection():
    raw_payload = request.form.get("payload") or request.args.get("payload")
    try:
        payload = InspectionPayload.from_raw(raw_payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400

    image_file = request.files.get("image")
    stream = image_file.stream if image_file else None
    ext = None
    if image_file and image_file.filename:
        ext = os.path.splitext(image_file.filename)[1]

    inspection = create_inspection_uc().execute(InspectionInput(
        lot_code=payload.lot_code,
        device_id=payload.device_id,
        detections=payload.detections,
        model_version=payload.model_version,
        image_stream=stream,
        image_extension=ext,
    ))
    return jsonify(inspection.to_dict()), 201


@inspection_bp.get("/lot/<lot_code>")
def list_by_lot(lot_code: str):
    limit = min(int(request.args.get("limit", 100)), 500)
    inspections = get_inspections_by_lot_uc().execute(lot_code, limit)
    return jsonify([i.to_dict() for i in inspections])


@inspection_bp.get("/lot/<lot_code>/latest")
def latest_by_lot(lot_code: str):
    inspection = get_latest_inspection_uc().execute(lot_code)
    if inspection is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(inspection.to_dict())


@inspection_bp.get("/<inspection_id>/image")
@require_role(UserRole.EXPORTER, UserRole.CONTROLLER, UserRole.ADMIN)
def get_image(inspection_id: str):
    inspection = get_inspection_by_id_uc().execute(inspection_id)
    if inspection is None or not inspection.image_path:
        return jsonify({"error": "not_found"}), 404
    try:
        abs_path = image_storage().get_absolute_path(inspection.image_path)
    except ValueError:
        return jsonify({"error": "invalid_path"}), 400
    if not os.path.exists(abs_path):
        return jsonify({"error": "file_missing"}), 404
    return send_file(abs_path)
