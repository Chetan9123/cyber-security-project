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

label_map = {
    "LABEL_0": "not_scam",
    "LABEL_1": "scam"
}


def classify_message(text: str):
    result = scam_classifier(text)[0]  # {'label': 'LABEL_1', 'score': 0.9}
    result["label"] = label_map.get(result["label"], result["label"])
    return result
