import json
import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.model.prediction_pipeline import predict_email

print("=== 1. VERIFY MODEL CLASS MAPPING ===")
try:
    with open('models/bert_phishing/config.json', 'r') as f:
        config = json.load(f)
    print("num_labels:", config.get("num_labels", 2))
    print("id2label:", config.get("id2label", "Not found"))
    print("label2id:", config.get("label2id", "Not found"))
except Exception as e:
    print("Error reading config.json:", e)

print("\n=== 2. VERIFY THE ACTIVE MODEL ===")
model_path = 'models/bert_phishing/model.safetensors'
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"Model safetensors size: {size_mb:.2f} MB")
else:
    print("model.safetensors not found.")

print("\n=== 3. TEST REAL LEGITIMATE EMAILS ===")
tests = [
    {
        "name": "TEST 1",
        "subject": "Weekly Project Meeting – Friday at 10:00 AM",
        "body": "Hi Team,\n\nThis is a reminder about our weekly project meeting scheduled for Friday at 10:00 AM. We will discuss the current development progress, pending tasks, and plans for next week.\n\nRegards,\nProject Team"
    },
    {
        "name": "TEST 2",
        "subject": "Your Project Documentation Is Ready",
        "body": "Hi Team,\n\nThe project documentation has been updated and is now available.\n\nYou can access the documentation here:\nhttps://docs.example.com/project/resources\n\nRegards,\nProject Team"
    },
    {
        "name": "TEST 3",
        "subject": "Monthly Project Status Update",
        "body": "Hello Team,\n\nPlease find the monthly project status update attached for your review.\n\nThe development team has completed the planned tasks for this month. We will discuss the remaining work during our next meeting.\n\nRegards,\nProject Manager"
    }
]

for t in tests:
    print(f"\n{t['name']}:")
    res = predict_email(t["subject"], t["body"])
    print("Legitimate probability:", res["legitimate_probability"])
    print("Malicious probability:", res["phishing_probability"])
    print("Prediction:", res["prediction"])
    print("Confidence:", res["confidence"])

print("\n=== 4. TEST MALICIOUS EMAILS ===")
malicious_test = {
    "subject": "URGENT ACTION REQUIRED: Your Account Will Be Suspended",
    "body": "Your account requires immediate verification.\n\nPlease verify your account immediately by providing your password, card information, CVV and OTP.\n\nVerify your account here:\nhttp://account-security-verification.example.com/secure-login"
}
res = predict_email(malicious_test["subject"], malicious_test["body"])
print("Legitimate probability:", res["legitimate_probability"])
print("Malicious probability:", res["phishing_probability"])
print("Prediction:", res["prediction"])
print("Confidence:", res["confidence"])

print("\n=== 5. CHECK THE PROBABILITY DISTRIBUTION ===")
df = pd.read_csv('data/processed/email_phishing_dataset.csv')
legit_samples = df[df['label'] == 0].head(100)
malic_samples = df[df['label'] == 1].head(100)

def get_probs(samples):
    probs = []
    for _, row in samples.iterrows():
        subject = str(row.get('subject', ''))
        if subject == 'nan': subject = ''
        body = str(row.get('text', ''))
        if body == 'nan': body = ''
        res = predict_email(subject, body)
        probs.append(res['phishing_probability'])
    return probs

legit_probs = get_probs(legit_samples)
malic_probs = get_probs(malic_samples)

print("LEGITIMATE:")
print("min malicious probability:", np.min(legit_probs))
print("max malicious probability:", np.max(legit_probs))
print("mean malicious probability:", np.mean(legit_probs))
print("median malicious probability:", np.median(legit_probs))

print("MALICIOUS:")
print("min malicious probability:", np.min(malic_probs))
print("max malicious probability:", np.max(malic_probs))
print("mean malicious probability:", np.mean(malic_probs))
print("median malicious probability:", np.median(malic_probs))
