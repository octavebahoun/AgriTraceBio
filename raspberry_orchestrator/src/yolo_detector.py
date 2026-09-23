"""Inférence YOLO Ultralytics sur les images capturées.

Deux modèles sont chargés : un pour la maturité et l'état général des
ananas, un pour la détection de taches/moisissures. Les résultats sont
fusionnés en une liste de détections normalisées.
"""
import logging
from typing import Optional
import numpy as np

from src.types import Detection

log = logging.getLogger(__name__)

# Correspondance labels modèle → classes attendues côté backend.
BACKEND_CLASSES = {
    "healthy", "unripe", "ripe", "overripe", "mold", "stained", "unknown",
}

RIPENESS_MAP = {
    "unripe": "unripe", "ripe": "ripe", "overripe": "overripe",
    "immature": "unripe", "mature": "ripe", "over_mature": "overripe",
}
MOLD_MAP = {
    "mold": "mold", "moisissure": "mold",
    "stain": "stained", "tache": "stained",
}


class YoloDetector:
    def __init__(self, ripeness_path: str, mold_path: str,
                 conf: float, imgsz: int):
        from ultralytics import YOLO
        self._ripeness = self._safe_load(YOLO, ripeness_path)
        self._mold = self._safe_load(YOLO, mold_path)
        self._conf = conf
        self._imgsz = imgsz

    def _safe_load(self, YOLO, path: Optional[str]):
        if not path:
            return None
        try:
            return YOLO(path)
        except Exception as e:
            log.warning("modèle indisponible (%s): %s", path, e)
            return None

    def detect(self, image_bytes: bytes) -> list[Detection]:
        import cv2
        arr = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            log.warning("image illisible")
            return []

        detections: list[Detection] = []
        detections.extend(self._run(self._ripeness, img, RIPENESS_MAP))
        detections.extend(self._run(self._mold, img, MOLD_MAP))
        return detections

    def _run(self, model, img, label_map: dict) -> list[Detection]:
        if model is None:
            return []
        try:
            results = model.predict(img, conf=self._conf,
                                    imgsz=self._imgsz, verbose=False)
        except Exception as e:
            log.warning("inférence échouée: %s", e)
            return []
        return _extract(results, label_map)


def _extract(results, label_map: dict) -> list[Detection]:
    detections: list[Detection] = []
    for res in results:
        names = res.names
        boxes = getattr(res, "boxes", None)
        if boxes is None:
            continue
        for i in range(len(boxes)):
            raw = str(names[int(boxes.cls[i])]).lower()
            mapped = label_map.get(raw, raw if raw in BACKEND_CLASSES
                                              else "unknown")
            xyxy = boxes.xyxy[i].tolist()
            detections.append(Detection(
                class_label=mapped,
                confidence=float(boxes.conf[i]),
                bbox=[float(x) for x in xyxy],
            ))
    return detections
