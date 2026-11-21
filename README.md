# Walled DLP

A local desktop DLP prototype for ChatGPT Web and Perplexity Web. It checks outgoing prompts and selected files for the exact marker `WALLED_SENSITIVE`. When detected, it asks for native desktop confirmation before allowing the browser interaction.

## Requirements

- Windows 10/11
- Python 3.12
- Chrome or Edge
- Tesseract OCR for image files (and OCR of scanned PDFs is not included in this MVP)

## Setup

1. Open PowerShell in this project folder.
2. Run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

For image OCR, install Tesseract for Windows. Then, if it is not on PATH, set its executable path near the top of `app/scanners/image_scanner.py`, for example:
`pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"`

3. Start the desktop app:

```powershell
python -m app.main
```

Keep it running. The local API listens only on `127.0.0.1:8765`.

4. Load the extension:
   - Open `chrome://extensions`
   - Enable Developer mode
   - Choose **Load unpacked**
   - Select the project's `extension` folder
   - Open the extension service worker's console if troubleshooting.

5. Copy the token from:
`%LOCALAPPDATA%\WalledDLP\token.txt`

Click the Walled DLP extension icon, paste this token into its popup, and choose Save token. It is stored in Chrome extension local storage.

6. Open `https://chatgpt.com` or `https://www.perplexity.ai` and test.

## Quick test

- Send a normal prompt: it should pass without a dialog.
- Send a prompt containing `WALLED_SENSITIVE`: the native dialog should appear.
- Choose Cancel: the prompt should not submit.
- Choose Continue: the prompt should submit.
- Upload a `.txt`, `.pdf`, or image containing the marker: the native dialog should appear.

Generate sample files with:

```powershell
python scripts/make_samples.py
```

## Important MVP limitations

- Website DOM and event handling change frequently. The selectors and event interception must be tested against current ChatGPT and Perplexity versions.
- File interception currently handles file-picker `change` events. Drag-and-drop, clipboard paste, and every possible upload pathway are not yet covered.
- Text PDFs are scanned with PyMuPDF. Scanned/image-only PDFs are held for safety and require an OCR enhancement before they can be approved automatically.
- Images use Tesseract OCR. Install Tesseract separately.
- The first version is designed for one browser profile and one local desktop session.
- The browser extension fails closed if the local scanner is unavailable.
- The response color is changed through DOM selectors and may need selector updates if either website changes its markup.

This is an assignment prototype, not a certified enterprise DLP product.
