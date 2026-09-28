import sys
import os

# Add src to sys.path to allow imports from utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.model.prediction_pipeline import predict_email
from src.utils.url_analyzer import analyze_email_urls

# Risk Configuration Thresholds
RISK_THRESHOLDS = {
    "high_prob": 0.50,
    "low_prob": 0.30,
    "strong_url_indicators_threshold": 2, # How many indicators to bump risk
}

def assess_email_risk(subject, body):
    """
    Combines BERT email classification and URL analysis to assess overall risk.
    """
    # 1. Run BERT Prediction
    try:
        prediction_result = predict_email(subject, body)
    except Exception as e:
        raise ValueError(f"Failed to generate BERT prediction: {e}")
        
    phish_prob = prediction_result.get("phishing_probability", 0.0)
    
    # 2. Run URL Analysis
    try:
        url_analysis = analyze_email_urls(subject, body)
    except Exception as e:
        raise ValueError(f"Failed to analyze URLs: {e}")
        
    urls_found = url_analysis.get("urls_found", 0)
    
    # Extract unique URL indicators across all URLs found
    url_indicators = set()
    extracted_urls = []
    total_indicator_count = 0
    
    for u in url_analysis.get("urls", []):
        url_val = u.get("url")
        if url_val and url_val not in extracted_urls:
            extracted_urls.append(url_val)
        for ind in u.get("suspicious_indicators", []):
            url_indicators.add(ind)
        total_indicator_count += u.get("indicator_count", 0)
        
    url_indicators = list(url_indicators)
    
    # 3. Determine Risk Level and Reasons
    risk_level = "LOW"
    risk_reasons = []
    
    # Check BERT signal
    if phish_prob >= RISK_THRESHOLDS["high_prob"]:
        risk_level = "HIGH"
        risk_reasons.append("High phishing probability from BERT model")
    elif phish_prob > RISK_THRESHOLDS["low_prob"]:
        risk_level = "MEDIUM"
        risk_reasons.append("Moderate phishing probability from BERT model")
    else:
        risk_level = "LOW"
        risk_reasons.append("Low phishing probability from BERT model")
        
    # Check URL signals
    has_strong_url_indicators = total_indicator_count >= RISK_THRESHOLDS["strong_url_indicators_threshold"]
    has_moderate_url_indicators = total_indicator_count > 0
    
    if has_strong_url_indicators:
        risk_reasons.append("Multiple suspicious URL characteristics detected")
        if risk_level == "MEDIUM":
            risk_level = "HIGH"
            risk_reasons.append("Elevated risk to HIGH due to strong URL indicators")
        elif risk_level == "LOW":
            risk_level = "MEDIUM"
            risk_reasons.append("Elevated risk to MEDIUM due to strong URL indicators")
    elif has_moderate_url_indicators:
        risk_reasons.append("Some suspicious URL characteristics detected")
        if risk_level == "LOW":
            risk_level = "MEDIUM"
            risk_reasons.append("Elevated risk to MEDIUM due to URL indicators")
            
    if urls_found == 0:
        risk_reasons.append("No URLs found in email content")
        
    # 4. Construct Final Output
    return {
        "prediction": prediction_result.get("prediction"),
        "phishing_probability": phish_prob,
        "legitimate_probability": prediction_result.get("legitimate_probability"),
        "confidence": prediction_result.get("confidence"),
        "risk_level": risk_level,
        "urls_found": urls_found,
        "extracted_urls": extracted_urls,
        "url_indicators": url_indicators,
        "risk_reasons": risk_reasons
    }
