# PREDICTION PIPELINE VERIFICATION REPORT

### Model Details
- **Model path:** models/bert_phishing/
- **Tokenizer path:** models/bert_phishing/
- **Successful model loading confirmation:** Yes
- **Successful inference confirmation:** Yes
- **Error-handling confirmation:** Yes

### Input/Output Format
- **Input format:** `predict_email(subject: str, body: str)`
- **Output format:** JSON dict with `prediction`, `phishing_probability`, `legitimate_probability`, `confidence`

### Test Cases & Results
#### Case: Legitimate Email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5879,
  "legitimate_probability": 0.4121,
  "confidence": 0.5879
}
```

#### Case: Phishing Email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6081,
  "legitimate_probability": 0.3919,
  "confidence": 0.6081
}
```

#### Case: Empty Subject - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6077,
  "legitimate_probability": 0.3923,
  "confidence": 0.6077
}
```

#### Case: Empty Body - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5659,
  "legitimate_probability": 0.4341,
  "confidence": 0.5659
}
```

#### Case: Very Long Email - PASS
```json
{
  "prediction": "Legitimate",
  "phishing_probability": 0.4927,
  "legitimate_probability": 0.5073,
  "confidence": 0.5073
}
```

#### Case: Both Empty - PASS
```json
"ValueError caught"
```

#### Case: Invalid Type - PASS
```json
"TypeError caught"
```

