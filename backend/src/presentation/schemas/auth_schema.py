"""Validation des payloads d'authentification."""
from dataclasses import dataclass

from src.domain.entities.user import UserRole
from src.presentation.schemas.lot_schema import _enum
from src.presentation.schemas.measurement_schema import (
    ValidationError,
    _str,
)


@dataclass
class RegisterInput:
    email: str
    password: str
    name: str
    role: UserRole

    @staticmethod
    def from_json(data: dict | None) -> "RegisterInput":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])

        email = _str(data, "email", errors, 3, 200)
        password = _str(data, "password", errors, 8, 200)
        name = _str(data, "name", errors, 1, 200)
        role = _enum(data, "role", UserRole, errors)

        if "@" not in email:
            errors.append({"field": "email", "msg": "invalid email"})

        if errors:
            raise ValidationError(errors)
        return RegisterInput(email, password, name, role)


@dataclass
class LoginInput:
    email: str
    password: str

    @staticmethod
    def from_json(data: dict | None) -> "LoginInput":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])
        email = _str(data, "email", errors, 3, 200)
        password = _str(data, "password", errors, 1, 200)
        if errors:
            raise ValidationError(errors)
        return LoginInput(email, password)
