"""Routes HTTP pour le QR code et la traçabilité publique."""
from flask import Blueprint, Response, jsonify

from src.presentation.routes.dependencies import (
    generate_qr_code_uc,
    get_lot_trace_uc,
)

qr_bp = Blueprint("qr", __name__, url_prefix="/api")


@qr_bp.get("/lots/code/<lot_code>/qr.svg")
def qr_svg(lot_code: str):
    result = generate_qr_code_uc().execute(lot_code)
    if result is None:
        return jsonify({"error": "not_found"}), 404
    return Response(result.svg, mimetype="image/svg+xml")


@qr_bp.get("/lots/code/<lot_code>/qr")
def qr_info(lot_code: str):
    result = generate_qr_code_uc().execute(lot_code)
    if result is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify({
        "lot_code": result.lot_code,
        "trace_url": result.trace_url,
        "svg_url": f"/api/lots/code/{result.lot_code}/qr.svg",
    })


@qr_bp.get("/public/trace/<lot_code>")
def public_trace(lot_code: str):
    trace = get_lot_trace_uc().execute(lot_code)
    if trace is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify({
        "lot": trace.lot.to_dict(),
        "measurements": [m.to_dict() for m in trace.measurements],
        "alerts": [a.to_dict() for a in trace.alerts],
        "inspections": [i.to_dict() for i in trace.inspections],
        "summary": {
            "total_measurements": len(trace.measurements),
            "total_alerts": len(trace.alerts),
            "critical_alerts": sum(
                1 for a in trace.alerts if a.level.value == "critical"
            ),
            "total_inspections": len(trace.inspections),
            "rejected_inspections": sum(
                1 for i in trace.inspections if i.verdict.value == "rejected"
            ),
        },
    })
