@echo off
cd /d "%~dp0\.."
py -3.12 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete. Install Tesseract OCR separately for image inspection.
pause
