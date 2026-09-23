"""Orchestrateur : capture → détection → envoi backend, en boucle."""
import logging
import time

from src.backend_client import BackendClient, BackendUnavailable, InspectionPost
from src.camera_client import CameraClient, CameraUnavailable
from src.config import config
from src.yolo_detector import YoloDetector

log = logging.getLogger(__name__)


class Orchestrator:
    def __init__(
        self,
        camera: CameraClient,
        detector: YoloDetector,
        backend: BackendClient,
    ):
        self._camera = camera
        self._detector = detector
        self._backend = backend

    def run_once(self) -> bool:
        try:
            image = self._camera.capture()
        except CameraUnavailable:
            return False

        detections = self._detector.detect(image.data)
        log.info("inspection: %d détections", len(detections))

        payload = InspectionPost(
            lot_code=config.current_lot_code,
            device_id=config.device_id,
            model_version=config.model_version,
            detections=detections,
            image_bytes=image.data,
            image_ext="jpg",
        )
        try:
            resp = self._backend.post_inspection(payload)
            log.info("backend OK: verdict=%s id=%s",
                     resp.get("verdict"), resp.get("id"))
            return True
        except BackendUnavailable:
            return False

    def run_forever(self) -> None:
        log.info("orchestrateur démarré (intervalle %ds)",
                 config.capture_interval_s)
        while True:
            try:
                self.run_once()
            except Exception as e:
                log.exception("cycle échoué: %s", e)
            time.sleep(config.capture_interval_s)
