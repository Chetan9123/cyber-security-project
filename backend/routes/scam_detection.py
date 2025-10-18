from fastapi import APIRouter
from schemas import ScamRequest, ScamResponse
from utils.classification_model import classify_message

router = APIRouter()

@router.post("/scam/", response_model=ScamResponse)
def detect_scam(request: ScamRequest):
    return classify_message(request.text)
