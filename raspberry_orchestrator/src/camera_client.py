"""Client HTTP pour tirer une image de l'ESP32-CAM."""
from dataclasses import dataclass
import logging
import requests

log = logging.getLogger(__name__)


class CameraUnavailable(Exception):
    pass


@dataclass
class CapturedImage:
    data: bytes
    content_type: str


class CameraClient:
    def __init__(self, base_url: str, timeout_s: float = 8.0):
        self._base = base_url.rstrip("/")
        self._timeout = timeout_s

    def capture(self) -> CapturedImage:
        url = f"{self._base}/capture"
        try:
            r = requests.get(url, timeout=self._timeout)
            r.raise_for_status()
        except requests.RequestException as e:
            log.warning("camera capture failed: %s", e)
            raise CameraUnavailable(str(e)) from e

        content_type = r.headers.get("Content-Type", "image/jpeg")
        if not content_type.startswith("image/"):
            raise CameraUnavailable(f"unexpected content-type: {content_type}")
        return CapturedImage(data=r.content, content_type=content_type)

    def health(self) -> bool:
        try:
            r = requests.get(f"{self._base}/health", timeout=2.0)
            return r.ok
        except requests.RequestException:
            return False
