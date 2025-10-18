# routes/complaint.py

from fastapi import APIRouter, HTTPException
from typing import List
from schemas import ComplaintOut, ComplaintIn  # adjust if your schemas file is named differently

router = APIRouter(
    prefix="/complaints",
    tags=["complaints"]
)

# Temporary in-memory storage for demonstration
complaints_db = []

@router.post("/", response_model=ComplaintOut)
def create_complaint(complaint: ComplaintIn):
    complaint_id = len(complaints_db) + 1
    new_complaint = ComplaintOut(id=complaint_id, **complaint.dict())
    complaints_db.append(new_complaint)
    return new_complaint

@router.get("/", response_model=List[ComplaintOut])
def get_all_complaints():
    return complaints_db

@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int):
    for complaint in complaints_db:
        if complaint.id == complaint_id:
            return complaint
    raise HTTPException(status_code=404, detail="Complaint not found")

@router.delete("/{complaint_id}", response_model=dict)
def delete_complaint(complaint_id: int):
    for i, complaint in enumerate(complaints_db):
        if complaint.id == complaint_id:
            complaints_db.pop(i)
            return {"detail": "Complaint deleted successfully"}
    raise HTTPException(status_code=404, detail="Complaint not found")
