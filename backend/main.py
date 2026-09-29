"""FastAPI app: upload -> analyze pipeline -> results.
Run from project root:  uvicorn backend.main:app --reload
"""
from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile

from backend import database as db
from backend.services.upload import save_upload
from backend.services.pdf_processor import to_image
from document_ai import ocr, classifier, entity_extractor
from security import ai_detector, tamper_detector, metadata_checker, risk_engine
from security.pii_masking import mask_cnic
from dashboard.validation import validate

app = FastAPI(title="Secure Document AI")
db.init_db()


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    out = []
    for f in files:
        doc_id = db.next_id()
        original = await save_upload(f, doc_id)
        try:
            image = to_image(original, doc_id)
        except Exception as e:
            raise HTTPException(400, f"Could not process {f.filename}: {e}")
        db.add_document(doc_id, f.filename, original, image)
        out.append({"document_id": doc_id, "filename": f.filename})
    return out


@app.post("/analyze/{document_id}")
def analyze(document_id: str):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(404, "Document not found")

    # Module 2: Document AI
    text, ocr_conf = ocr.run_ocr(doc["image_path"])
    doc_type, cls_conf = classifier.classify(text)
    entities = entity_extractor.extract(text)

    # Module 3: Security
    ai_prob = ai_detector.ai_probability(doc["image_path"])
    tamper = tamper_detector.tamper_score(doc["image_path"])
    meta_score, meta_reasons = metadata_checker.check(doc["original_path"])
    security = risk_engine.compute(ai_prob, tamper, meta_score, meta_reasons)

    # Module 4: validation (on RAW values), then mask PII for output
    validation = validate(doc_type, entities, db.roll_numbers(exclude_id=document_id))
    entities["cnic"] = mask_cnic(entities.get("cnic"))

    result = {
        "document_id": document_id,
        "filename": doc["filename"],
        "document_type": doc_type,
        "classification_confidence": cls_conf,
        "ocr_confidence": ocr_conf,
        "entities": entities,
        "security": security,
        "validation": validation,
    }
    db.save_result(document_id, result)
    return result


@app.get("/documents")
def documents():
    return db.list_documents()


@app.get("/documents/{document_id}")
def document(document_id: str):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@app.get("/statistics")
def statistics():
    stats = {"total": 0, "analyzed": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for d in db.list_documents():
        stats["total"] += 1
        if d["result"]:
            stats["analyzed"] += 1
            stats[d["result"]["security"]["risk_level"]] += 1
    return stats
