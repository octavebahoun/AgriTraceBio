"""Use case : authentifier un utilisateur et générer un JWT."""
from dataclasses import dataclass
from typing import Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.password_hasher import PasswordHasher
from src.domain.services.token_service import TokenClaims, TokenService


@dataclass
class AuthResult:
    user: User
    token: str


class LoginUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self._repository = repository
        self._hasher = hasher
        self._token_service = token_service

    def execute(self, email: str, password: str) -> Optional[AuthResult]:
        user = self._repository.find_by_email(email)
        if user is None:
            return None
        if not self._hasher.verify(password, user.password_hash):
            return None
        assert user.id is not None
        token = self._token_service.encode(
            TokenClaims(user_id=user.id, role=user.role.value, email=user.email)
        )
        return AuthResult(user=user, token=token)
