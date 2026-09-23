"""Entité User : compte d'un acteur de la plateforme."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    EXPORTER = "exporter"
    CONTROLLER = "controller"


@dataclass
class User:
    email: str
    password_hash: str
    name: str
    role: UserRole
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: Optional[str] = None

    def to_public_dict(self) -> dict:
        data = asdict(self)
        data.pop("password_hash")
        data["role"] = self.role.value
        data["created_at"] = self.created_at.isoformat()
        if self.id is None:
            data.pop("id")
        return data
