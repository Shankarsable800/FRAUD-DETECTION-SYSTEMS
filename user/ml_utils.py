
import joblib
import os
import numpy as np

# Load model and scaler from disk
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'fraud_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'ml', 'scaler.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def extract_features(data):
    amount = float(data.get("amount", 0))
    recipient_length = len(data.get("recipient", ""))
    description = data.get("description", "").lower()
    has_keyword_urgent = 1 if "urgent" in description else 0
    return [amount, recipient_length, has_keyword_urgent]

def predict_fraud(data):
    features = extract_features(data)
    scaled_features = scaler.transform([features])
    fraud_score = model.predict_proba(scaled_features)[0][1]
    is_fraud = fraud_score > 0.5
    return fraud_score, is_fraud
