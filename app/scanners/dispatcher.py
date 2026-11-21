from .base import ScanResult
from .text_scanner import scan_text
from .pdf_scanner import scan_pdf
from .image_scanner import scan_image

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".log"}

def scan_file(filename: str, mime_type: str, data: bytes) -> ScanResult:
    lower = (filename or "").lower()
    if lower.endswith(".pdf") or mime_type == "application/pdf":
        return scan_pdf(data)
    if lower.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")) or mime_type.startswith("image/"):
        return scan_image(data)
    if lower.endswith(tuple(TEXT_EXTENSIONS)) or mime_type.startswith("text/"):
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
        return scan_text(text)
    raise ValueError("Unsupported file type. Supported: TXT, MD, CSV, PDF and common image formats.")
