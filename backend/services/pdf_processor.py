"""Turn an uploaded file into a PNG image the AI modules can read."""
from pathlib import Path
import fitz  # PyMuPDF
import cv2

PROCESSED_DIR = Path("data/processed")


def to_image(original_path: Path, doc_id: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / f"{doc_id}.png"
    if original_path.suffix.lower() == ".pdf":
        with fitz.open(original_path) as pdf:            # first page only
            pdf[0].get_pixmap(dpi=200).save(str(out))
    else:
        img = cv2.imread(str(original_path))
        if img is None:
            raise ValueError("Could not read image file")
        cv2.imwrite(str(out), img)
    return out
