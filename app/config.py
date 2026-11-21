from pathlib import Path
import secrets

APP_NAME = "Walled DLP"
MARKER = "WALLED_SENSITIVE"
HOST = "127.0.0.1"
PORT = 8765
MAX_FILE_BYTES = 12 * 1024 * 1024
REQUEST_TIMEOUT_SECONDS = 180

DATA_DIR = Path.home() / "AppData" / "Local" / "WalledDLP"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = DATA_DIR / "token.txt"
LOG_FILE = DATA_DIR / "walled-dlp.log"

def load_or_create_token() -> str:
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if token:
            return token
    token = secrets.token_urlsafe(32)
    TOKEN_FILE.write_text(token, encoding="utf-8")
    return token

API_TOKEN = load_or_create_token()
