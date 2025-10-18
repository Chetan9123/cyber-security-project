from pydantic import BaseModel
from typing import Optional

# -------------------------------
# Complaint Schemas
# -------------------------------

class ComplaintIn(BaseModel):
    title: str
    description: str
    reporter_name: Optional[str] = None
    reporter_email: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


class ComplaintOut(BaseModel):
    id: int
    title: str
    description: str
    reporter_name: Optional[str] = None
    reporter_email: Optional[str] = None
    created_at: Optional[str] = None  # ISO datetime string

    class Config:
        from_attributes = True

# -------------------------------
# Scam Detection Schema
# -------------------------------

class ScamDetectionOut(BaseModel):
    message: str
    label: str  # 'scam' or 'not_scam'
    score: float  # confidence score

    class Config:
        from_attributes = True

class ScamRequest(BaseModel):
    text: str

class ScamResponse(BaseModel):
    label: str
    score: float

