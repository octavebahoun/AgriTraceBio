"""Routes HTTP pour la génération et le téléchargement des certificats PDF."""
from flask import Blueprint, Response, jsonify

from src.domain.entities.user import UserRole
from src.presentation.middleware.auth_middleware import require_role
from src.presentation.routes.dependencies import generate_certificate_uc

certificate_bp = Blueprint("certificates", __name__, url_prefix="/api/certificates")


@certificate_bp.get("/lot/<lot_code>.pdf")
@require_role(UserRole.EXPORTER, UserRole.CONTROLLER, UserRole.ADMIN)
def download(lot_code: str):
    result = generate_certificate_uc().execute(lot_code)
    if result is None:
        return jsonify({"error": "not_found"}), 404

    filename = f"certificat_{result.lot_code}.pdf"
    return Response(
        result.pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(result.pdf_bytes)),
        },
    )
