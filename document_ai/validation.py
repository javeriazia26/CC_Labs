"""Field validation. Returns {"status": PASS|WARN|FAIL, "errors": [], "warnings": []}"""
import re
from datetime import datetime


def _valid_date(s):
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%d-%m-%y"):
        try:
            datetime.strptime(s, fmt)
            return True
        except ValueError:
            pass
    return False


def validate(doc_type, entities, existing_roll_numbers=()):
    errors, warnings = [], []
    if doc_type == "Unknown":
        warnings.append("Document type could not be identified")
    required = {"BSEK Slip": ["name", "roll_number"], "CNIC": ["name", "cnic"], "Receipt": ["date"]}
    for f in required.get(doc_type, []):
        if not entities.get(f):
            errors.append(f"Missing required field: {f}")
    if entities.get("cnic") and not re.fullmatch(r"\d{5}-?\d{7}-?\d", entities["cnic"]):
        errors.append("Invalid CNIC format")
    if entities.get("date") and not _valid_date(entities["date"]):
        errors.append("Invalid date")
    if entities.get("roll_number") in existing_roll_numbers:
        errors.append("Duplicate roll number found in another document")
    for f in ("father_name",):
        if doc_type == "BSEK Slip" and not entities.get(f):
            warnings.append(f"Missing optional field: {f}")
    status = "FAIL" if errors else "WARN" if warnings else "PASS"
    return {"status": status, "errors": errors, "warnings": warnings}
