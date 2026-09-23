"""Configuration centralisée depuis .env."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    esp32_cam_url: str = os.getenv("ESP32_CAM_URL", "http://192.168.1.50")
    backend_url: str = os.getenv("BACKEND_URL", "http://192.168.1.42:5000")

    device_id: str = os.getenv("DEVICE_ID", "raspi-01")
    current_lot_code: str = os.getenv("CURRENT_LOT_CODE", "AGR-001")

    model_ripeness_path: str = os.getenv(
        "MODEL_RIPENESS_PATH", "./models/pineapple_ripeness_v1.pt")
    model_mold_path: str = os.getenv(
        "MODEL_MOLD_PATH", "./models/pineapple_mold_v1.pt")
    model_version: str = os.getenv("MODEL_VERSION", "yolov8n-agritrace-v1")

    yolo_conf: float = float(os.getenv("YOLO_CONF_THRESHOLD", "0.35"))
    yolo_imgsz: int = int(os.getenv("YOLO_IMG_SIZE", "640"))

    capture_interval_s: int = int(os.getenv("CAPTURE_INTERVAL_S", "60"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
