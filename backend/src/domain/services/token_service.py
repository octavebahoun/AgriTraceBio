"""Génération et validation de tokens JWT."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt


@dataclass
class TokenClaims:
    user_id: str
    role: str
    email: str


class TokenService:
    def __init__(self, secret: str, algorithm: str, expires_hours: int):
        self._secret = secret
        self._algorithm = algorithm
        self._expires_hours = expires_hours

    def encode(self, claims: TokenClaims) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": claims.user_id,
            "role": claims.role,
            "email": claims.email,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=self._expires_hours)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> Optional[TokenClaims]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except jwt.PyJWTError:
            return None
        return TokenClaims(
            user_id=str(payload.get("sub")),
            role=str(payload.get("role")),
            email=str(payload.get("email")),
        )
