import os
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

load_dotenv()

# Hugging Face token
hf_token = os.getenv("HF_TOKEN")

# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection", use_auth_token=hf_token
)
model = AutoModelForSequenceClassification.from_pretrained(
    "mrm8488/bert-tiny-finetuned-sms-spam-detection", use_auth_token=hf_token
)

# Initialize pipeline
scam_classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1  # CPU (-1) or GPU (0)
)

def classify_message(text: str):
    """
    Returns a dict: {'label': 'spam'/'ham', 'score': float}
    """
    result = scam_classifier(text)
    return {"label": result[0]["label"], "score": result[0]["score"]}
