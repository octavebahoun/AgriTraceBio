"""Interface abstraite pour la génération de certificats PDF."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.alert import Alert
from src.domain.entities.block import Block
from src.domain.entities.inspection import Inspection
from src.domain.entities.lot import Lot
from src.domain.entities.measurement import Measurement


@dataclass
class CertificateInput:
    lot: Lot
    measurements: list[Measurement]
    alerts: list[Alert]
    inspections: list[Inspection]
    blockchain: list[Block]
    trace_url: str


class CertificateGenerator(ABC):
    @abstractmethod
    def generate(self, data: CertificateInput) -> bytes:
        ...
