"""Configuration centralisée chargée depuis les variables d'environnement."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    flask_env: str = os.getenv("FLASK_ENV", "development")
    flask_host: str = os.getenv("FLASK_HOST", "0.0.0.0")
    flask_port: int = int(os.getenv("FLASK_PORT", "5000"))

    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME", "agritracebio")

    public_base_url: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:5173")

    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-production-please")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expires_hours: int = int(os.getenv("JWT_EXPIRES_HOURS", "24"))

    uploads_dir: str = os.getenv("UPLOADS_DIR", "./uploads")
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "10"))

    @property
    def debug(self) -> bool:
        return self.flask_env == "development"


config = Config()
