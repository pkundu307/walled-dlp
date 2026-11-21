# Architecture

## Components

1. **Chrome/Edge Manifest V3 extension**
   - Content scripts observe prompt submission and file selection on ChatGPT and Perplexity.
   - The service worker sends inspection requests to the local Python API.
   - The response-style observer applies a CSS class to detected assistant response containers.

2. **Local FastAPI service**
   - Binds only to `127.0.0.1`.
   - Requires a random bearer token stored under `%LOCALAPPDATA%\WalledDLP\token.txt`.
   - Inspects prompt text and uploaded file bytes.
   - Waits for a user decision only when the marker is detected or inspection cannot safely complete.

3. **Scanner modules**
   - Plain text: UTF-8 decoding and exact marker search (case-insensitive).
   - PDF: PyMuPDF text extraction.
   - Image: Pillow + Tesseract OCR.

4. **Native desktop UI**
   - Tkinter creates a native desktop confirmation window.
   - A thread-safe queue serializes dialogs.
   - The API request waits for Continue or Cancel.

## Enforcement flow

### Prompt
The extension captures click and Enter submission events, stops the original event, and asks the local service to scan the composer text. If the service allows the request, the extension replays the user action. If canceled or inspection fails, it does not replay the action.

### File
The extension captures the file input `change` event before page listeners, reads the selected file locally, and sends its bytes to the local scanner. It stops propagation while inspection is pending. On Continue, it dispatches a new `change` event so the web app can process the selected file. On Cancel, it clears the input.

### Response styling
A MutationObserver watches for new response nodes and adds a CSS class to site-specific response containers. The class changes text color without modifying response content.

## Security and limitations

- The local API binds to loopback and uses a random bearer token.
- The API does not log prompt or file contents.
- Inspection failures are handled fail-closed.
- This MVP does not cover every upload path (for example drag-and-drop and clipboard).
- Scanned PDFs are not OCR'd in this initial version; they are held for safety.
- Website DOM changes can require selector updates.
