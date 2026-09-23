"""Use case : créer un compte utilisateur."""
from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self._repository = repository
        self._hasher = hasher

    def execute(self, email: str, password: str, name: str, role: UserRole) -> User:
        user = User(
            email=email.lower().strip(),
            password_hash=self._hasher.hash(password),
            name=name.strip(),
            role=role,
        )
        return self._repository.save(user)
