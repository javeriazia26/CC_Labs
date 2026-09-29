"""Validate and save uploaded files."""
from pathlib import Path
from fastapi import HTTPException
from backend.models import ALLOWED_EXTENSIONS, MAX_FILE_MB

UPLOAD_DIR = Path("data/uploads")


async def save_upload(file, doc_id: str) -> Path:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}")
    content = await file.read()
    if len(content) > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(400, f"File too large (max {MAX_FILE_MB} MB)")
    if not content:
        raise HTTPException(400, "Empty file")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{doc_id}{ext}"
    path.write_bytes(content)
    return path
