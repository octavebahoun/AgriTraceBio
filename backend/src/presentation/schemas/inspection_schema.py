"""Validation du payload d'inspection YOLO."""
import json
from dataclasses import dataclass

from src.domain.entities.inspection import Detection, InspectionClass
from src.presentation.schemas.measurement_schema import ValidationError, _str


@dataclass
class InspectionPayload:
    lot_code: str
    device_id: str
    model_version: str
    detections: list[Detection]

    @staticmethod
    def from_raw(raw: str | None) -> "InspectionPayload":
        if not raw:
            raise ValidationError([{"field": "payload", "msg": "payload required"}])
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ValidationError([{"field": "payload", "msg": "invalid JSON"}])
        return InspectionPayload.from_json(data)

    @staticmethod
    def from_json(data: dict | None) -> "InspectionPayload":
        errors: list[dict] = []
        if not isinstance(data, dict):
            raise ValidationError([{"field": "body", "msg": "JSON object required"}])

        lot_code = _str(data, "lot_code", errors, 1, 50)
        device_id = _str(data, "device_id", errors, 1, 100)
        model_version = _str(data, "model_version", errors, 1, 50)
        detections = _parse_detections(data.get("detections"), errors)

        if errors:
            raise ValidationError(errors)
        return InspectionPayload(lot_code, device_id, model_version, detections)


def _parse_detections(raw, errors) -> list[Detection]:
    if not isinstance(raw, list):
        errors.append({"field": "detections", "msg": "list required"})
        return []
    detections: list[Detection] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            errors.append({"field": f"detections[{i}]", "msg": "object required"})
            continue
        cls = item.get("class_label")
        conf = item.get("confidence")
        bbox = item.get("bbox")
        try:
            cls_e = InspectionClass(cls)
        except (ValueError, TypeError):
            errors.append({"field": f"detections[{i}].class_label",
                          "msg": f"one of {[c.value for c in InspectionClass]}"})
            continue
        if not isinstance(conf, (int, float)) or not 0.0 <= float(conf) <= 1.0:
            errors.append({"field": f"detections[{i}].confidence",
                          "msg": "number in [0,1]"})
            continue
        if (not isinstance(bbox, list) or len(bbox) != 4
                or not all(isinstance(x, (int, float)) for x in bbox)):
            errors.append({"field": f"detections[{i}].bbox",
                          "msg": "[x1,y1,x2,y2] numbers"})
            continue
        detections.append(Detection(class_label=cls_e, confidence=float(conf),
                                    bbox=[float(x) for x in bbox]))
    return detections
