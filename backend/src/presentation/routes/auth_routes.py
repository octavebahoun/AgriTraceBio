"""Routes HTTP pour l'authentification."""
from flask import Blueprint, g, jsonify, request

from src.infrastructure.repositories.mongo_user_repository import EmailAlreadyExists
from src.presentation.middleware.auth_middleware import require_auth
from src.presentation.routes.dependencies import (
    login_user_uc,
    register_user_uc,
    user_repository,
)
from src.presentation.schemas.auth_schema import (
    LoginInput,
    RegisterInput,
    ValidationError,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    try:
        payload = RegisterInput.from_json(request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400

    try:
        user = register_user_uc().execute(
            email=payload.email,
            password=payload.password,
            name=payload.name,
            role=payload.role,
        )
    except EmailAlreadyExists:
        return jsonify({"error": "email_already_exists"}), 409
    return jsonify(user.to_public_dict()), 201


@auth_bp.post("/login")
def login():
    try:
        payload = LoginInput.from_json(request.get_json(silent=True))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors}), 400

    result = login_user_uc().execute(payload.email, payload.password)
    if result is None:
        return jsonify({"error": "invalid_credentials"}), 401
    return jsonify({
        "token": result.token,
        "user": result.user.to_public_dict(),
    })


@auth_bp.get("/me")
@require_auth
def me():
    user = user_repository().find_by_id(g.current_user_id)
    if user is None:
        return jsonify({"error": "user_not_found"}), 404
    return jsonify(user.to_public_dict())
