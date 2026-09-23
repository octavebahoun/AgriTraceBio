"""Use cases : lecture et vérification de la blockchain."""
from src.domain.entities.block import Block
from src.domain.repositories.blockchain_repository import BlockchainRepository
from src.domain.services.blockchain_service import BlockchainService, VerifyResult


class ListBlockchainUseCase:
    def __init__(self, repository: BlockchainRepository):
        self._repository = repository

    def execute(self, limit: int = 500) -> list[Block]:
        return self._repository.list_all(limit)


class GetBlockchainByLotUseCase:
    def __init__(self, repository: BlockchainRepository):
        self._repository = repository

    def execute(self, lot_code: str, limit: int = 500) -> list[Block]:
        return self._repository.find_by_lot(lot_code, limit)


class VerifyBlockchainUseCase:
    def __init__(self, service: BlockchainService):
        self._service = service

    def execute(self) -> VerifyResult:
        return self._service.verify_chain()
