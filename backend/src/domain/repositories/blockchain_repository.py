"""Interface abstraite pour la persistance de la chaîne de blocs."""
from abc import ABC, abstractmethod
from typing import Iterator, Optional

from src.domain.entities.block import Block


class BlockchainRepository(ABC):
    @abstractmethod
    def append(self, block: Block) -> Block:
        ...

    @abstractmethod
    def get_last(self) -> Optional[Block]:
        ...

    @abstractmethod
    def list_all(self, limit: int = 500) -> list[Block]:
        ...

    @abstractmethod
    def find_by_lot(self, lot_code: str, limit: int = 500) -> list[Block]:
        ...

    @abstractmethod
    def iter_ordered(self) -> Iterator[Block]:
        """Itère les blocs dans l'ordre croissant d'index (pour vérification)."""
        ...
