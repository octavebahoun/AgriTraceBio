"""Point d'entrée : construit les dépendances et démarre la boucle."""
import logging
import signal
import sys

from src.backend_client import BackendClient
from src.camera_client import CameraClient
from src.config import config
from src.orchestrator import Orchestrator
from src.yolo_detector import YoloDetector


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-5s %(name)s: %(message)s",
    )


def build_orchestrator() -> Orchestrator:
    camera = CameraClient(config.esp32_cam_url)
    detector = YoloDetector(
        ripeness_path=config.model_ripeness_path,
        mold_path=config.model_mold_path,
        conf=config.yolo_conf,
        imgsz=config.yolo_imgsz,
    )
    backend = BackendClient(config.backend_url)
    return Orchestrator(camera, detector, backend)


def install_signal_handlers() -> None:
    def stop(signum, _frame):
        logging.info("signal %s reçu, arrêt propre", signum)
        sys.exit(0)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)


def main() -> None:
    setup_logging()
    install_signal_handlers()
    orchestrator = build_orchestrator()
    orchestrator.run_forever()


if __name__ == "__main__":
    main()
