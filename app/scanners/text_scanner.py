from .base import ScanResult
from app.config import MARKER

def scan_text(text: str) -> ScanResult:
    found = MARKER.casefold() in (text or "").casefold()
    return ScanResult(
        scanned=True,
        sensitive=found,
        reason=f"Marker {MARKER} detected" if found else "",
        extracted_chars=len(text or ""),
    )
