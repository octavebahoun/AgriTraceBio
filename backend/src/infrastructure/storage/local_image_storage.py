"""Stockage local (disque) des images d'inspection."""
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO

from src.domain.services.image_storage import ImageStorage

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}


class LocalImageStorage(ImageStorage):
    def __init__(self, base_dir: str):
        self._base = Path(base_dir).resolve()
        (self._base / "inspections").mkdir(parents=True, exist_ok=True)

    def save(self, lot_code: str, stream: BinaryIO, extension: str) -> str:
        ext = extension.lower().lstrip(".")
        if ext not in ALLOWED_EXT:
            raise ValueError(f"unsupported extension: {extension}")

        now = datetime.now(timezone.utc)
        subdir = self._base / "inspections" / now.strftime("%Y/%m/%d")
        subdir.mkdir(parents=True, exist_ok=True)

        safe_lot = "".join(c for c in lot_code if c.isalnum() or c in "-_")[:40]
        filename = f"{safe_lot}_{now.strftime('%H%M%S')}_{secrets.token_hex(4)}.{ext}"
        target = subdir / filename

        with open(target, "wb") as f:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                f.write(chunk)

        return str(target.relative_to(self._base))

    def get_absolute_path(self, storage_path: str) -> str:
        target = (self._base / storage_path).resolve()
        if not str(target).startswith(str(self._base)):
            raise ValueError("path traversal detected")
        return str(target)
