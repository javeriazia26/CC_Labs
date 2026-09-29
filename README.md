# Secure Document AI — Ingestion & Authenticity Analysis (Hackathon MVP)

Upload PDF/image → OCR → classify → extract entities → tamper/AI/metadata checks → mask PII → validate → risk score → dashboard.

> Outputs are **risk indicators**, not proof that a document is fake. `ai_detector.py` is a labelled heuristic prototype (image-noise uniformity), not a trained detector.

## Setup
1. Install **Tesseract OCR** (Windows: https://github.com/UB-Mannheim/tesseract/wiki, default path `C:\Program Files\Tesseract-OCR`).
   Add it to PATH, or set: `set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`
2. `python -m venv .venv` then activate it (`.venv\Scripts\activate` on Windows)
3. `pip install -r requirements.txt`

## Run (two terminals, from the project root)
```
uvicorn backend.main:app --reload          # API on :8000  (docs at /docs)
streamlit run dashboard/app.py             # UI on :8501
```
Tests: `pytest`

## Endpoints
POST /upload · POST /analyze/{id} · GET /documents · GET /documents/{id} · GET /statistics

## Data format
See `backend/schemas.py`. Only addition to the agreed JSON: `filename` and `ocr_confidence`.

## Troubleshooting
- `TesseractNotFoundError`: Tesseract not installed / not on PATH → set `TESSERACT_CMD`.
- `ModuleNotFoundError: backend`: run commands from the project root.
- Low OCR confidence: use clearer scans (≥150 DPI).
- Dashboard says backend unreachable: start uvicorn first.
