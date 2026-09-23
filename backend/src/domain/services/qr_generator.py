"""Génère l'URL publique et le QR code SVG associé à un lot."""
from io import BytesIO
import qrcode
from qrcode.image.svg import SvgImage


class QrGenerator:
    def __init__(self, public_base_url: str):
        self._base = public_base_url.rstrip("/")

    def build_trace_url(self, lot_code: str) -> str:
        return f"{self._base}/trace/{lot_code}"

    def generate_svg(self, lot_code: str) -> bytes:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(self.build_trace_url(lot_code))
        qr.make(fit=True)
        img = qr.make_image(image_factory=SvgImage)
        buf = BytesIO()
        img.save(buf)
        return buf.getvalue()
