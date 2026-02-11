from pydantic import BaseModel
from typing import Any


class StructuredRecord(BaseModel):
    medicine: str | None = None
    dosage: str | None = None
    frequency: str | None = None
    labName: str | None = None
    labValue: str | None = None
    normalRange: str | None = None
    confidence: float | None = None


class ReportResponse(BaseModel):
    id: int
    original_filename: str
    structured_data: list[StructuredRecord]
    decision_support: dict[str, Any]
    explanation: str
