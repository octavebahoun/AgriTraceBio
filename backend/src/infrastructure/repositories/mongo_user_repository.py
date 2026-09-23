"""Implémentation MongoDB du UserRepository."""
from typing import Optional
from bson import ObjectId
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import UserRepository


class EmailAlreadyExists(Exception):
    pass


class MongoUserRepository(UserRepository):
    COLLECTION = "users"

    def __init__(self, db: Database):
        self._collection = db[self.COLLECTION]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self._collection.create_index("email", unique=True)

    def save(self, user: User) -> User:
        data = {
            "email": user.email.lower(),
            "password_hash": user.password_hash,
            "name": user.name,
            "role": user.role.value,
            "created_at": user.created_at,
        }
        try:
            result = self._collection.insert_one(data)
        except DuplicateKeyError:
            raise EmailAlreadyExists(user.email)
        user.id = str(result.inserted_id)
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            doc = self._collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        return _to_entity(doc) if doc else None

    def find_by_email(self, email: str) -> Optional[User]:
        doc = self._collection.find_one({"email": email.lower()})
        return _to_entity(doc) if doc else None


def _to_entity(doc: dict) -> User:
    return User(
        id=str(doc["_id"]),
        email=doc["email"],
        password_hash=doc["password_hash"],
        name=doc["name"],
        role=UserRole(doc["role"]),
        created_at=doc["created_at"],
    )
