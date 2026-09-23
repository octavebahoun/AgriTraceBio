"""Client HTTP pour POST vers le backend AgriTraceBio."""
import io
import json
import logging
from dataclasses import dataclass
from typing import Optional
import requests

from src.types import Detection

log = logging.getLogger(__name__)


class BackendUnavailable(Exception):
    pass


@dataclass
class InspectionPost:
    lot_code: str
    device_id: str
    model_version: str
    detections: list[Detection]
    image_bytes: Optional[bytes] = None
    image_ext: str = "jpg"


class BackendClient:
    def __init__(self, base_url: str, timeout_s: float = 15.0):
        self._base = base_url.rstrip("/")
        self._timeout = timeout_s

    def post_inspection(self, insp: InspectionPost) -> dict:
        url = f"{self._base}/api/inspections"
        payload = {
            "lot_code": insp.lot_code,
            "device_id": insp.device_id,
            "model_version": insp.model_version,
            "detections": [{
                "class_label": d.class_label,
                "confidence": d.confidence,
                "bbox": d.bbox,
            } for d in insp.detections],
        }

        files = {"payload": (None, json.dumps(payload), "application/json")}
        if insp.image_bytes:
            files["image"] = (
                f"capture.{insp.image_ext}",
                io.BytesIO(insp.image_bytes),
                f"image/{insp.image_ext}",
            )
        try:
            r = requests.post(url, files=files, timeout=self._timeout)
            r.raise_for_status()
        except requests.RequestException as e:
            log.warning("backend POST failed: %s", e)
            raise BackendUnavailable(str(e)) from e
        return r.json()

    def health(self) -> bool:
        try:
            r = requests.get(f"{self._base}/api/health", timeout=2.0)
            return r.ok
        except requests.RequestException:
            return False
