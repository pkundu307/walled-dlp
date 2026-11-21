import base64
import hmac
import logging
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from app.config import API_TOKEN, MAX_FILE_BYTES
from app.scanners.text_scanner import scan_text
from app.scanners.dispatcher import scan_file
from app.decision_queue import DecisionQueue

logger = logging.getLogger("walled_dlp")

class PromptRequest(BaseModel):
    text: str = Field(max_length=200_000)
    page: str = "unknown"

class FileRequest(BaseModel):
    filename: str = Field(max_length=255)
    mime_type: str = "application/octet-stream"
    data_base64: str
    page: str = "unknown"

def create_app(decisions: DecisionQueue) -> FastAPI:
    api = FastAPI(title="Walled DLP Local API", docs_url=None, redoc_url=None)

    def authenticate(authorization: str | None):
        expected = f"Bearer {API_TOKEN}"
        if not authorization or not hmac.compare_digest(authorization, expected):
            raise HTTPException(status_code=401, detail="Unauthorized")

    @api.get("/health")
    def health():
        return {"status": "ok"}

    @api.post("/v1/scan/prompt")
    def inspect_prompt(payload: PromptRequest, authorization: str | None = Header(default=None)):
        authenticate(authorization)
        result = scan_text(payload.text)
        if not result.sensitive:
            return {"allow": True, "sensitive": False}
        logger.warning("Sensitive prompt detected page=%s", payload.page)
        decision = decisions.ask("prompt", f"Website: {payload.page}", result.reason)
        return {"allow": decision == "continue", "sensitive": True}

    @api.post("/v1/scan/file")
    def inspect_file(payload: FileRequest, authorization: str | None = Header(default=None)):
        authenticate(authorization)
        try:
            data = base64.b64decode(payload.data_base64, validate=True)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid file encoding")
        if len(data) > MAX_FILE_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds 12 MB inspection limit")
        try:
            result = scan_file(payload.filename, payload.mime_type, data)
        except (ValueError, RuntimeError) as exc:
            logger.warning("File inspection failed filename=%s type=%s", payload.filename, type(exc).__name__)
            # Fail closed if inspection cannot be completed.
            decision = decisions.ask("file", payload.filename, str(exc))
            return {"allow": decision == "continue", "sensitive": True, "inspection_error": True}
        if not result.sensitive:
            return {"allow": True, "sensitive": False}
        logger.warning("Sensitive file detected filename=%s page=%s", payload.filename, payload.page)
        decision = decisions.ask("file", payload.filename, result.reason or "Sensitive marker detected")
        return {"allow": decision == "continue", "sensitive": True}

    return api
