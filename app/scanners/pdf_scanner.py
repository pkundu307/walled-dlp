import fitz
from .base import ScanResult
from .text_scanner import scan_text

def scan_pdf(data: bytes) -> ScanResult:
    try:
        doc = fitz.open(stream=data, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
    except Exception as exc:
        raise ValueError(f"Could not read PDF: {type(exc).__name__}") from exc

    result = scan_text(text)
    if not text.strip():
        # Scanned/image-only PDFs need OCR; fail closed rather than silently allowing.
        return ScanResult(
            scanned=False,
            sensitive=True,
            reason="PDF contains no extractable text; OCR is required, so upload was held for safety.",
            extracted_chars=0,
        )
    return result
