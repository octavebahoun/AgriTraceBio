"""Client MongoDB singleton pour l'application."""
from pymongo import MongoClient
from pymongo.database import Database

from config import config


class MongoConnection:
    _client: MongoClient | None = None
    _db: Database | None = None

    @classmethod
    def connect(cls) -> Database:
        if cls._db is None:
            cls._client = MongoClient(config.mongo_uri, serverSelectionTimeoutMS=5000)
            cls._db = cls._client[config.mongo_db_name]
        return cls._db

    @classmethod
    def close(cls) -> None:
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def ping(cls) -> bool:
        try:
            cls.connect().command("ping")
            return True
        except Exception:
            return False


def get_db() -> Database:
    return MongoConnection.connect()
