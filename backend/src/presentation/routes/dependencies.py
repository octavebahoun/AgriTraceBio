"""Injection de dépendances pour les routes."""
from functools import lru_cache

from config import config
from src.application.use_cases.blockchain_queries import (
    GetBlockchainByLotUseCase,
    ListBlockchainUseCase,
    VerifyBlockchainUseCase,
)
from src.application.use_cases.create_inspection import CreateInspectionUseCase
from src.application.use_cases.create_lot import CreateLotUseCase
from src.application.use_cases.create_measurement import CreateMeasurementUseCase
from src.application.use_cases.generate_certificate import GenerateCertificateUseCase
from src.application.use_cases.generate_qr_code import GenerateQrCodeUseCase
from src.application.use_cases.get_inspections import (
    GetInspectionByIdUseCase,
    GetInspectionsByLotUseCase,
    GetLatestInspectionUseCase,
)
from src.application.use_cases.get_alerts import (
    GetActiveAlertsUseCase,
    GetAlertsByLotUseCase,
    ResolveAlertUseCase,
)
from src.application.use_cases.get_lot_trace import GetLotTraceUseCase
from src.application.use_cases.get_lots import (
    GetLotByCodeUseCase,
    GetLotByIdUseCase,
    ListLotsUseCase,
    UpdateLotStatusUseCase,
)
from src.application.use_cases.get_measurements import (
    GetLatestMeasurementUseCase,
    GetMeasurementsByLotUseCase,
)
from src.application.use_cases.login_user import LoginUserUseCase
from src.application.use_cases.process_measurement import ProcessMeasurementUseCase
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.services.alert_detector import AlertDetector
from src.domain.services.blockchain_service import BlockchainService
from src.domain.services.password_hasher import PasswordHasher
from src.domain.services.qr_generator import QrGenerator
from src.domain.services.token_service import TokenService
from src.domain.services.verdict_calculator import VerdictCalculator
from src.infrastructure.database.mongo_client import get_db
from src.infrastructure.repositories.mongo_alert_repository import MongoAlertRepository
from src.infrastructure.repositories.mongo_blockchain_repository import (
    MongoBlockchainRepository,
)
from src.infrastructure.repositories.mongo_inspection_repository import (
    MongoInspectionRepository,
)
from src.infrastructure.repositories.mongo_lot_repository import MongoLotRepository
from src.infrastructure.repositories.mongo_measurement_repository import (
    MongoMeasurementRepository,
)
from src.infrastructure.repositories.mongo_user_repository import MongoUserRepository
from src.infrastructure.pdf.reportlab_certificate_generator import (
    ReportlabCertificateGenerator,
)
from src.infrastructure.storage.local_image_storage import LocalImageStorage


@lru_cache(maxsize=1)
def measurement_repository() -> MongoMeasurementRepository:
    return MongoMeasurementRepository(get_db())


@lru_cache(maxsize=1)
def alert_repository() -> MongoAlertRepository:
    return MongoAlertRepository(get_db())


@lru_cache(maxsize=1)
def alert_detector() -> AlertDetector:
    return AlertDetector()


@lru_cache(maxsize=1)
def blockchain_repository() -> MongoBlockchainRepository:
    return MongoBlockchainRepository(get_db())


@lru_cache(maxsize=1)
def blockchain_service() -> BlockchainService:
    return BlockchainService(blockchain_repository())


@lru_cache(maxsize=1)
def lot_repository() -> MongoLotRepository:
    return MongoLotRepository(get_db())


def create_lot_uc() -> CreateLotUseCase:
    return CreateLotUseCase(lot_repository(), blockchain_service())


def get_lot_by_id_uc() -> GetLotByIdUseCase:
    return GetLotByIdUseCase(lot_repository())


def get_lot_by_code_uc() -> GetLotByCodeUseCase:
    return GetLotByCodeUseCase(lot_repository())


def list_lots_uc() -> ListLotsUseCase:
    return ListLotsUseCase(lot_repository())


def update_lot_status_uc() -> UpdateLotStatusUseCase:
    return UpdateLotStatusUseCase(lot_repository(), blockchain_service())


@lru_cache(maxsize=1)
def qr_generator() -> QrGenerator:
    return QrGenerator(config.public_base_url)


def generate_qr_code_uc() -> GenerateQrCodeUseCase:
    return GenerateQrCodeUseCase(lot_repository(), qr_generator())


def get_lot_trace_uc() -> GetLotTraceUseCase:
    return GetLotTraceUseCase(
        lot_repository(),
        measurement_repository(),
        alert_repository(),
        inspection_repository(),
    )


@lru_cache(maxsize=1)
def user_repository() -> MongoUserRepository:
    return MongoUserRepository(get_db())


@lru_cache(maxsize=1)
def password_hasher() -> PasswordHasher:
    return PasswordHasher()


@lru_cache(maxsize=1)
def token_service() -> TokenService:
    return TokenService(
        secret=config.jwt_secret,
        algorithm=config.jwt_algorithm,
        expires_hours=config.jwt_expires_hours,
    )


def register_user_uc() -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository(), password_hasher())


def login_user_uc() -> LoginUserUseCase:
    return LoginUserUseCase(user_repository(), password_hasher(), token_service())


@lru_cache(maxsize=1)
def inspection_repository() -> MongoInspectionRepository:
    return MongoInspectionRepository(get_db())


@lru_cache(maxsize=1)
def image_storage() -> LocalImageStorage:
    return LocalImageStorage(config.uploads_dir)


@lru_cache(maxsize=1)
def verdict_calculator() -> VerdictCalculator:
    return VerdictCalculator()


def create_inspection_uc() -> CreateInspectionUseCase:
    return CreateInspectionUseCase(
        inspection_repository(),
        image_storage(),
        verdict_calculator(),
        blockchain_service(),
    )


def list_blockchain_uc() -> ListBlockchainUseCase:
    return ListBlockchainUseCase(blockchain_repository())


def get_blockchain_by_lot_uc() -> GetBlockchainByLotUseCase:
    return GetBlockchainByLotUseCase(blockchain_repository())


def verify_blockchain_uc() -> VerifyBlockchainUseCase:
    return VerifyBlockchainUseCase(blockchain_service())


@lru_cache(maxsize=1)
def certificate_generator() -> ReportlabCertificateGenerator:
    return ReportlabCertificateGenerator()


def generate_certificate_uc() -> GenerateCertificateUseCase:
    return GenerateCertificateUseCase(
        lot_repository(),
        measurement_repository(),
        alert_repository(),
        inspection_repository(),
        blockchain_repository(),
        qr_generator(),
        certificate_generator(),
    )


def get_inspections_by_lot_uc() -> GetInspectionsByLotUseCase:
    return GetInspectionsByLotUseCase(inspection_repository())


def get_latest_inspection_uc() -> GetLatestInspectionUseCase:
    return GetLatestInspectionUseCase(inspection_repository())


def get_inspection_by_id_uc() -> GetInspectionByIdUseCase:
    return GetInspectionByIdUseCase(inspection_repository())


def create_measurement_uc() -> CreateMeasurementUseCase:
    return CreateMeasurementUseCase(measurement_repository())


def process_measurement_uc() -> ProcessMeasurementUseCase:
    return ProcessMeasurementUseCase(
        measurement_repository(),
        alert_repository(),
        alert_detector(),
        blockchain_service(),
    )


def get_measurements_uc() -> GetMeasurementsByLotUseCase:
    return GetMeasurementsByLotUseCase(measurement_repository())


def get_latest_measurement_uc() -> GetLatestMeasurementUseCase:
    return GetLatestMeasurementUseCase(measurement_repository())


def get_alerts_by_lot_uc() -> GetAlertsByLotUseCase:
    return GetAlertsByLotUseCase(alert_repository())


def get_active_alerts_uc() -> GetActiveAlertsUseCase:
    return GetActiveAlertsUseCase(alert_repository())


def resolve_alert_uc() -> ResolveAlertUseCase:
    return ResolveAlertUseCase(alert_repository())
