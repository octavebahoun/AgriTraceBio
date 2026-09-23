"""Calcule un verdict global à partir de la liste des détections YOLO."""
from src.domain.entities.inspection import (
    Detection,
    InspectionClass,
    InspectionVerdict,
)

REJECTED_CLASSES = {InspectionClass.MOLD, InspectionClass.OVERRIPE}
WARNING_CLASSES = {InspectionClass.STAINED, InspectionClass.UNRIPE}

MIN_CONFIDENCE = 0.35


class VerdictCalculator:
    def compute(self, detections: list[Detection]) -> InspectionVerdict:
        for d in detections:
            if d.confidence < MIN_CONFIDENCE:
                continue
            if d.class_label in REJECTED_CLASSES:
                return InspectionVerdict.REJECTED
        for d in detections:
            if d.confidence < MIN_CONFIDENCE:
                continue
            if d.class_label in WARNING_CLASSES:
                return InspectionVerdict.WARNING
        return InspectionVerdict.OK
