"""Pydantic models describing the fixed JSON structure shared by all modules."""
from typing import Dict, List, Optional
from pydantic import BaseModel


class Security(BaseModel):
    ai_probability: float
    tamper_score: float
    risk_score: int
    risk_level: str
    reasons: List[str] = []


class Validation(BaseModel):
    status: str
    errors: List[str] = []
    warnings: List[str] = []


class DocumentResult(BaseModel):
    document_id: str
    filename: Optional[str] = None
    document_type: str
    classification_confidence: float
    ocr_confidence: float = 0.0          # extra field (dashboard needs it)
    entities: Dict[str, Optional[str]]
    security: Security
    validation: Validation
