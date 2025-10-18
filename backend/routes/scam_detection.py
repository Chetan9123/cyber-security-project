from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
import requests
import re
from dotenv import load_dotenv
from typing import Optional 

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
EMAIL_API_KEY = os.getenv("ABSTRACT_EMAIL_API_KEY")
PHONE_API_KEY = os.getenv("ABSTRACT_PHONE_API_KEY")

# Hugging Face model
tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection", use_auth_token=HF_TOKEN
)
model = AutoModelForSequenceClassification.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection", use_auth_token=HF_TOKEN
)
scam_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

router = APIRouter()

# Pydantic schemas
class ScamRequest(BaseModel):
    text: str

class ScamResponse(BaseModel):
    label: str
    score: float
    email_check: Optional[str] = None
    phone_check: Optional[str] = None

# Label mapping
label_map = {"LABEL_0": "not_scam", "LABEL_1": "scam"}

# Regex
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PHONE_REGEX = r"\+?\d[\d -]{7,}\d"

# Helper functions
def check_email(email: str) -> str:
    if not EMAIL_API_KEY:
        return "unknown"
    try:
        res = requests.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key={EMAIL_API_KEY}&email={email}"
        ).json()
        return "safe" if res.get("deliverability") == "DELIVERABLE" else "scammer"
    except:
        return "unknown"

def check_phone(phone: str) -> str:
    if not PHONE_API_KEY:
        return "unknown"
    try:
        res = requests.get(
            f"https://phonevalidation.abstractapi.com/v1/?api_key={PHONE_API_KEY}&phone={phone}"
        ).json()
        return "safe" if res.get("valid") else "scammer"
    except:
        return "unknown"

@router.post("/scam/", response_model=ScamResponse)
def detect_scam(request: ScamRequest):
    text = request.text or ""

    # Hugging Face detection
    try:
        hf_result = scam_classifier(text)[0]
        label = label_map.get(hf_result["label"], hf_result["label"])
        score = hf_result["score"]
    except Exception:
        label = "error"
        score = 0.0

    # Check email/phone
    email_match = re.search(EMAIL_REGEX, text)
    phone_match = re.search(PHONE_REGEX, text)

    email_check = check_email(email_match.group()) if email_match else None
    phone_check = check_phone(phone_match.group()) if phone_match else None

    return ScamResponse(
        label=label,
        score=score,
        email_check=email_check,
        phone_check=phone_check
    )
