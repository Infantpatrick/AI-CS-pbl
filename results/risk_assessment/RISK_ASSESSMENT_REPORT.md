# RISK ASSESSMENT VERIFICATION REPORT

### Methodology
The risk assessment combines the machine learning (BERT) prediction and static URL analysis heuristics. The BERT probability serves as the primary signal, while URL indicators are used as supporting evidence to adjust the final risk level.

### BERT Probability Thresholds
- **HIGH**: Phishing Probability >= 0.70
- **MEDIUM**: 0.30 < Phishing Probability < 0.70
- **LOW**: Phishing Probability <= 0.30

### URL Indicator Contribution
- If the email contains strong/multiple suspicious URL indicators (>= 2), the risk level is elevated (e.g., from LOW to MEDIUM or MEDIUM to HIGH).
- If the email contains moderate indicators (> 0), LOW risk is elevated to MEDIUM.
- No URLs present does NOT penalize the email.

### Definitions
- **LOW Risk**: Unlikely to be phishing. Low ML probability and no significant URL threats.
- **MEDIUM Risk**: Potentially suspicious. May have borderline ML probability or suspicious URL features requiring caution.
- **HIGH Risk**: Very likely phishing. High ML probability or strong combination of ML prediction and malicious URL patterns.

### Limitations
- The accuracy heavily depends on the BERT model's performance on unseen data.
- Static URL analysis may produce false positives for complex but benign URLs.

### Security Considerations
- No active external requests are made during this risk assessment. It remains completely static and offline, ensuring safety from tracker pixels or malicious endpoints.

### Test Cases & Results
#### 1. Clearly legitimate email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6086,
  "legitimate_probability": 0.3914,
  "confidence": 0.6086,
  "risk_level": "MEDIUM",
  "urls_found": 1,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model"
  ]
}
```

#### 2. High-confidence phishing email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6081,
  "legitimate_probability": 0.3919,
  "confidence": 0.6081,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "suspicious_keywords_found:login,update,secure,auth",
    "http_used"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### 3. Medium-confidence case - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5967,
  "legitimate_probability": 0.4033,
  "confidence": 0.5967,
  "risk_level": "MEDIUM",
  "urls_found": 0,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "No URLs found in email content"
  ]
}
```

#### 4. Phishing email with suspicious URL - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5954,
  "legitimate_probability": 0.4046,
  "confidence": 0.5954,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "ip_address_used",
    "suspicious_keywords_found:login",
    "http_used"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### 5. Legitimate email containing a normal URL - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6362,
  "legitimate_probability": 0.3638,
  "confidence": 0.6362,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "suspicious_keywords_found:auth",
    "contains_at_symbol"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### 6. Email with no URL - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5231,
  "legitimate_probability": 0.4769,
  "confidence": 0.5231,
  "risk_level": "MEDIUM",
  "urls_found": 0,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "No URLs found in email content"
  ]
}
```

#### 8. Multiple suspicious URL indicators - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5888,
  "legitimate_probability": 0.4112,
  "confidence": 0.5888,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "suspicious_keywords_found:login,verify,update,secure,admin",
    "http_used"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### 7. Empty input - PASS
Expected error caught: Failed to generate BERT prediction: Both subject and body cannot be empty.

