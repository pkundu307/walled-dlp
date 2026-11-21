from io import BytesIO
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
from .base import ScanResult
from .text_scanner import scan_text

def scan_image(data: bytes) -> ScanResult:
    try:
        image = Image.open(BytesIO(data)).convert("RGB")
        text = pytesseract.image_to_string(image)
    except pytesseract.pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR is not installed. Install it and set the Tesseract path, then retry."
        ) from exc
    except Exception as exc:
        raise ValueError(f"Could not inspect image: {type(exc).__name__}") from exc
    return scan_text(text)
