"""Décorateurs d'authentification et d'autorisation pour Flask."""
from functools import wraps

from flask import g, jsonify, request

from src.domain.entities.user import UserRole
from src.presentation.routes.dependencies import token_service


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = _extract_claims()
        if claims is None:
            return jsonify({"error": "unauthorized"}), 401
        g.current_user_id = claims.user_id
        g.current_user_role = claims.role
        g.current_user_email = claims.email
        return fn(*args, **kwargs)
    return wrapper


def require_role(*allowed: UserRole):
    allowed_values = {r.value for r in allowed}

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = _extract_claims()
            if claims is None:
                return jsonify({"error": "unauthorized"}), 401
            if claims.role not in allowed_values:
                return jsonify({"error": "forbidden"}), 403
            g.current_user_id = claims.user_id
            g.current_user_role = claims.role
            g.current_user_email = claims.email
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def _extract_claims():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    if not token:
        return None
    return token_service().decode(token)
