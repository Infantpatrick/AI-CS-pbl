import os
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizerFast
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.preprocessing.text_formatter import format_bert_text

class PhishingPredictor:
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/bert_phishing'))
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        try:
            self.model = BertForSequenceClassification.from_pretrained(model_dir)
            self.model.to(self.device)
            self.model.eval()
            self.tokenizer = BertTokenizerFast.from_pretrained(model_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to load model or tokenizer from {model_dir}. Error: {e}")

    def predict_email(self, subject, body):
        # 1. Input Validation and Type Checking
        if not isinstance(subject, str) and subject is not None:
            raise TypeError("Subject must be a string or None.")
        if not isinstance(body, str) and body is not None:
            raise TypeError("Body must be a string or None.")
            
        subject = subject.strip() if subject else ""
        body = body.strip() if body else ""
        
        # Handle "Both fields empty"
        if not subject and not body:
            raise ValueError("Both subject and body cannot be empty.")
            
        # 2. Combine exactly as done during training using canonical formatter
        bert_text = format_bert_text(subject, body)
        
        # 3. Tokenization
        # Max length 256 to match training. 
        # Truncation=True handles very long emails safely.
        inputs = self.tokenizer(
            bert_text,
            padding='max_length',
            truncation=True,
            max_length=256,
            return_tensors='pt'
        )
        
        # Move to correct device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 4. Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            
        # 5. Calculate Probabilities
        probs = F.softmax(logits, dim=1).cpu().numpy()[0]
        legitimate_prob = float(probs[0])
        phishing_prob = float(probs[1])
        
        # 6. Final Prediction
        is_phishing = phishing_prob > 0.50
        prediction_label = "Phishing" if is_phishing else "Legitimate"
        confidence = phishing_prob if is_phishing else legitimate_prob
        
        # 7. Return Structured Result
        return {
            "prediction": prediction_label,
            "phishing_probability": round(phishing_prob, 4),
            "legitimate_probability": round(legitimate_prob, 4),
            "confidence": round(confidence, 4)
        }

# For simple functional access as requested
_predictor_instance = None

def predict_email(subject, body):
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = PhishingPredictor()
    return _predictor_instance.predict_email(subject, body)
