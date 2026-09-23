"""Tests unitaires basiques : payload correctement formaté."""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.backend_client import BackendClient, InspectionPost
from src.types import Detection


def test_post_inspection_serializes_payload_and_image():
    client = BackendClient("http://backend")
    payload = InspectionPost(
        lot_code="AGR-001",
        device_id="raspi-01",
        model_version="v1",
        detections=[Detection("mold", 0.87, [10, 20, 80, 90])],
        image_bytes=b"\xff\xd8\xff",
        image_ext="jpg",
    )

    with patch("src.backend_client.requests.post") as post:
        post.return_value = MagicMock(ok=True,
                                      json=lambda: {"id": "abc",
                                                    "verdict": "rejected"})
        post.return_value.raise_for_status = lambda: None

        result = client.post_inspection(payload)

        args, kwargs = post.call_args
        assert args[0] == "http://backend/api/inspections"
        files = kwargs["files"]
        assert "payload" in files
        assert "image" in files
        raw_payload = json.loads(files["payload"][1])
        assert raw_payload["lot_code"] == "AGR-001"
        assert len(raw_payload["detections"]) == 1
        assert raw_payload["detections"][0]["class_label"] == "mold"
        assert result["verdict"] == "rejected"


if __name__ == "__main__":
    test_post_inspection_serializes_payload_and_image()
    print("OK   test_post_inspection_serializes_payload_and_image")
