"""Interface abstraite pour stocker les images d'inspection."""
from abc import ABC, abstractmethod
from typing import BinaryIO


class ImageStorage(ABC):
    @abstractmethod
    def save(self, lot_code: str, stream: BinaryIO, extension: str) -> str:
        """Enregistre l'image et retourne un chemin/identifiant."""
        ...

    @abstractmethod
    def get_absolute_path(self, storage_path: str) -> str:
        ...
