# BACKEND API VERIFICATION REPORT

### Architecture
FastAPI-based RESTful API serving the Phase 12 risk assessment module. It leverages Pydantic for schema validation, ensuring valid inputs before model inference.

### API Endpoints
- **GET `/health`**: Returns API status.
- **GET `/model-info`**: Returns basic metadata about the loaded BERT model.
- **POST `/predict`**: Processes email subject and body and returns risk assessment.

### Model Loading Approach
The fine-tuned BERT model and tokenizer are instantiated lazily on the first request (or module import in Phase 10 logic) and reused for all subsequent requests to avoid loading overhead per request.

### Validation Rules
- Subject and Body must be valid strings.
- Maximum input constraints enforced (1000 for subject, 50000 for body).
- At least one field (subject or body) must contain text (prevent empty evaluations).

### Test Cases & Results
#### GET /health - PASS
```json
{
  "status": "healthy"
}
```

#### GET /model-info - PASS
```json
{
  "model": "BERT",
  "model_type": "bert-base-uncased fine-tuned for phishing classification",
  "status": "loaded"
}
```

#### Legitimate Email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6251,
  "legitimate_probability": 0.3749,
  "confidence": 0.6251,
  "risk_level": "MEDIUM",
  "urls_found": 0,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "No URLs found in email content"
  ]
}
```

#### Phishing Email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6105,
  "legitimate_probability": 0.3895,
  "confidence": 0.6105,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "http_used",
    "suspicious_keywords_found:login,update,secure"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### Suspicious URL - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5549,
  "legitimate_probability": 0.4451,
  "confidence": 0.5549,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    "http_used",
    "ip_address_used",
    "suspicious_keywords_found:admin"
  ],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "Multiple suspicious URL characteristics detected",
    "Elevated risk to HIGH due to strong URL indicators"
  ]
}
```

#### No URL - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.6214,
  "legitimate_probability": 0.3786,
  "confidence": 0.6214,
  "risk_level": "MEDIUM",
  "urls_found": 0,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "No URLs found in email content"
  ]
}
```

#### Empty Input - PASS
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body"
      ],
      "msg": "Value error, Both subject and body cannot be empty.",
      "input": {
        "subject": "",
        "body": ""
      },
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

#### Missing fields - PASS
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "body"
      ],
      "msg": "Field required",
      "input": {
        "subject": "Hello"
      }
    }
  ]
}
```

#### Invalid input - PASS
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": [
        "body",
        "subject"
      ],
      "msg": "Input should be a valid string",
      "input": [
        "Not a string"
      ]
    }
  ]
}
```

#### Long email - PASS
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.5947,
  "legitimate_probability": 0.4053,
  "confidence": 0.5947,
  "risk_level": "MEDIUM",
  "urls_found": 0,
  "url_indicators": [],
  "risk_reasons": [
    "Moderate phishing probability from BERT model",
    "No URLs found in email content"
  ]
}
```

