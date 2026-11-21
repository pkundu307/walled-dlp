from dataclasses import dataclass

@dataclass
class ScanResult:
    scanned: bool
    sensitive: bool
    reason: str = ""
    extracted_chars: int = 0
