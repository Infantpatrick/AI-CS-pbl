# AI-Based Email Phishing Detection Using BERT

## 1. Project Title
**AI-Based Email Phishing Detection Using BERT**

## 2. Project Overview
This project provides a comprehensive end-to-end system for detecting phishing emails. The system accepts an email subject and body, uses a fine-tuned BERT model to classify the email as Phishing or Legitimate, extracts and statically analyzes any URLs, and combines these signals to generate a final LOW, MEDIUM, or HIGH risk assessment. The results are served via a FastAPI backend and displayed on a modern React/Vite web interface. 
*(Note: The system performs static URL analysis only and does not perform live URL reputation checking or web scraping).*

## 3. Problem Statement
Phishing attacks remain one of the most prominent cybersecurity threats, often relying on deceptive language and malicious URLs to compromise systems and steal sensitive information. Traditional rule-based filters struggle to keep up with the evolving linguistic tactics of attackers. There is a critical need for an intelligent system that understands context and language nuances to detect these threats accurately.

## 4. Objectives
- Develop an AI model capable of accurately differentiating between legitimate and phishing emails using NLP.
- Extract and analyze embedded URLs without executing or visiting them to identify suspicious heuristics.
- Combine NLP-based classification with static URL analysis to provide an overall risk assessment.
- Provide a robust API and an intuitive, modern dashboard to visualize the threat assessment and model confidence.

## 5. Key Features
- **BERT NLP Classification:** Uses a fine-tuned `bert-base-uncased` model for deep contextual analysis of email content.
- **Static URL Analysis:** Extracts HTTP/HTTPS links and analyzes their length, domain characteristics, and patterns for suspicious indicators.
- **Integrated Risk Assessment:** Combines model probability and URL indicators to classify emails into LOW, MEDIUM, or HIGH risk tiers.
- **FastAPI Backend:** A scalable, typed, and well-documented REST API for interacting with the detection pipeline.
- **Modern React Frontend:** A responsive, glassmorphism-styled dashboard built with Vite and Tailwind CSS.
- **Comprehensive Evaluation:** Detailed model evaluation and error analysis on a held-out test set.

## 6. System Architecture
```text
User
 ↓
React + Vite Frontend
 ↓
FastAPI /predict
 ↓
Risk Assessment
 ↓
BERT Prediction + URL Analysis
 ↓
Risk Result
 ↓
FastAPI JSON Response
 ↓
React Results Dashboard
```

## 7. Complete Workflow
```text
Dataset
 ↓
Cleaning
 ↓
EDA
 ↓
Train/Validation/Test Split
 ↓
BERT Tokenization
 ↓
BERT Fine-Tuning
 ↓
Evaluation
 ↓
Error Analysis
 ↓
Model Saving
 ↓
Prediction Pipeline
```

## 8. Dataset Information
The model was trained and evaluated on a diverse combination of public datasets:
- **Sources:** CEAS, Enron, Ling-Spam, Nazario, Nigerian Fraud, SpamAssassin, Phishing Email dataset.
- **Raw emails:** 101,136
- **Duplicates removed:** 13,250
- **Final cleaned dataset:** 87,886
- **Legitimate:** 43,459
- **Phishing:** 44,427

## 9. Data Preprocessing
Emails were heavily cleaned to remove HTML tags, standardize newline characters, handle missing subject lines, and strip unnecessary metadata. Duplicates were removed to prevent data leakage and model overfitting.

## 10. Exploratory Data Analysis
EDA revealed differences in email length, vocabulary distribution, and common structural patterns (e.g., urgency keywords, excessive links) between legitimate and phishing emails, informing the tokenization and feature extraction steps.

## 11. Train/Validation/Test Split
The dataset was split to ensure rigorous, unbiased evaluation:
- **Total:** 87,886
- **Train:** 70,308 (80%)
- **Validation:** 8,789 (10%)
- **Test:** 8,789 (10%) - *Used strictly for final evaluation.*

## 12. BERT Tokenization
Using Hugging Face's `BertTokenizer`, text was tokenized with a maximum sequence length (typically 128 or 256 tokens depending on training config) with padding and truncation to convert textual data into input IDs and attention masks suitable for BERT.

## 13. BERT Model Architecture
- **Model:** `bert-base-uncased`
- **Task:** Binary email classification
- **Framework:** PyTorch
- **Library:** Hugging Face Transformers
```text
Email
 ↓
BERT Tokenizer
 ↓
Input IDs + Attention Mask
 ↓
BERT Encoder
 ↓
[CLS] Representation
 ↓
Classification Head
 ↓
Phishing / Legitimate
```

## 14. Model Training
The model was fine-tuned on the training set using the AdamW optimizer. The learning rate, batch size, and epochs were optimized through the validation set to maximize recall and overall F1-score while preventing overfitting.

## 15. Model Evaluation
The final fine-tuned model was evaluated strictly on the 8,789 held-out test samples. 
*These are TEST SET results:*
- **Accuracy:** 67.58%
- **Precision:** 61.28%
- **Recall:** 97.48%
- **F1-score:** 75.25%

**Confusion Matrix:**
- **True Negatives (TN):** 1609
- **False Positives (FP):** 2737
- **False Negatives (FN):** 112
- **True Positives (TP):** 4331

## 16. Error Analysis
- **False Positives:** 2,737
- **False Negatives:** 112
- **False Positive Rate:** 62.98%
- **False Negative Rate:** 2.52%

*Explanation:* 
False positives are legitimate emails incorrectly flagged as phishing (often due to automated alerts, password reset requests, or short texts mimicking phishing). False negatives are phishing emails that successfully evaded detection (often due to highly obfuscated text or sophisticated corporate masking).

## 17. Prediction Pipeline
A modular prediction pipeline (`predict_email`) encapsulates the tokenizer and the fine-tuned PyTorch model. It preprocesses raw text, performs inference, applies a softmax function to extract probabilities, and returns structured confidence scores.

## 18. URL Extraction & Analysis
The URL analyzer extracts all plain-text and protocol-prefixed URLs from the email body. The analysis is strictly **static**:
- The application does **NOT** visit, download, or execute URL content.
- Extracts features such as domain name, length, and HTTPS usage.
- Identifies heuristic suspicious indicators (e.g., IP addresses as domains, long subdomains).
*Note: Heuristic indicators are flags for suspicion, not definitive proof of malicious activity.*

## 19. Risk Assessment
The risk assessment module (`assess_email_risk`) integrates BERT prediction and URL indicators.
- BERT classification serves as the primary signal.
- URL indicators act as supporting evidence.
- Outputs a definitive Risk Level (**LOW**, **MEDIUM**, or **HIGH**) alongside explanatory risk reasons.

## 20. Backend API
The backend is built with FastAPI and Uvicorn, featuring Pydantic validation, error handling, and CORS configuration.
- `GET /health` - API status.
- `GET /model-info` - Loaded model metadata.
- `POST /predict` - Core analysis endpoint.

## 21. Frontend
A modern dashboard built with React, Vite, Tailwind CSS, and Lucide React.
Key UI features include:
- Glassmorphism Email Input Form
- Simulated Analysis Loading State
- Prediction Result & Probability Progress Bars
- Risk Level Badges & Risk Reasons Breakdown
- URL Analysis Summary Cards
- Model Statistics & Responsive Design

## 22. Frontend + Backend Integration
The React frontend communicates directly with the FastAPI backend via Axios. Environment variables (`VITE_API_URL`) configure the endpoint, and robust error handling ensures graceful degradation if the backend is offline or returns validation errors (e.g., 422).

## 23. End-to-End Testing
The complete system underwent rigorous E2E testing (Phase 16).
- **Total tests:** 19
- **Passed:** 19
- **Failed:** 0
- **Errors:** 0
Verified components include the API, CORS, UI responsiveness, security boundaries, prediction mapping, and production builds.

## 24. Project Structure
```text
├── backend/
│   ├── app.py
│   └── schemas.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── tokenized/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── models/
│   └── bert_phishing/
├── results/
│   ├── evaluation/
│   ├── error_analysis/
│   └── ...
├── src/
│   ├── data/
│   ├── features/
│   ├── model/
│   └── utils/
├── requirements.txt
└── README.md
```

## 25. Technology Stack
- **Machine Learning:** PyTorch, Hugging Face Transformers, Scikit-learn, Pandas, NumPy
- **Backend API:** Python, FastAPI, Uvicorn, Pydantic
- **Frontend UI:** JavaScript/JSX, React, Vite, Tailwind CSS, Lucide React, Axios

## 26. Installation

### Python Environment & Backend
```bash
# Clone the repository and navigate to the root directory
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
pip install fastapi uvicorn httpx
```

### Frontend Dependencies
```bash
cd frontend
npm install
```

## 27. Configuration
Ensure the backend is accessible by configuring the frontend environment. Create a `.env` file in the `frontend/` directory:
```env
VITE_API_URL=http://localhost:8000
```

## 28. How to Run

You will need two separate terminal windows.

**Terminal 1 (Backend):**
```bash
# From the project root
python -m uvicorn backend.app:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
# From the frontend directory
cd frontend
npm run dev
```
Navigate to `http://localhost:5173` in your browser.

## 29. API Usage

### Example Request (`POST /predict`)
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"subject": "URGENT: Verify your account", "body": "Please click here to verify your details: http://suspicious-login.com"}'
```

### Example Response
```json
{
  "prediction": "Phishing",
  "phishing_probability": 0.98,
  "legitimate_probability": 0.02,
  "confidence": 0.98,
  "risk_level": "HIGH",
  "urls_found": 1,
  "url_indicators": [
    {
      "url": "http://suspicious-login.com",
      "domain": "suspicious-login.com",
      "url_length": 27,
      "uses_https": false,
      "indicators": ["Uses HTTP instead of HTTPS"]
    }
  ],
  "risk_reasons": [
    "High phishing probability (98%)",
    "Suspicious URL characteristics detected"
  ]
}
```

## 30. Screenshots
*(Placeholder: Add screenshots of the interface here)*
- **Homepage:** `[Screenshot Placeholder]`
- **Email Analyzer:** `[Screenshot Placeholder]`
- **Phishing Result:** `[Screenshot Placeholder]`
- **Legitimate Result:** `[Screenshot Placeholder]`
- **URL Analysis:** `[Screenshot Placeholder]`
- **Risk Assessment:** `[Screenshot Placeholder]`
- **FastAPI Swagger (`/docs`):** `[Screenshot Placeholder]`
- **Model Performance:** `[Screenshot Placeholder]`

## 31. Model Performance
**Accuracy:** 67.58% | **Precision:** 61.28% | **Recall:** 97.48% | **F1 Score:** 75.25%

## 32. Limitations
- **High False-Positive Rate:** At ~63%, the model is highly aggressive in classifying emails as phishing. While this maximizes threat detection (high recall), it necessitates manual whitelisting or secondary filters in a production environment to prevent alert fatigue.
- **Static URL Analysis:** The system relies purely on heuristics and regex. It does not perform live DNS lookups or check reputation databases (e.g., VirusTotal).
- **CPU Inference:** Without GPU acceleration, inference on large batches or extremely long emails may incur latency.

## 33. Future Improvements
- **Threshold Optimization & FP Reduction:** Adjust probability thresholds or integrate a secondary meta-classifier to reduce false positives.
- **Live Threat-Intelligence Verification:** Integrate third-party API checks for URL reputation.
- **Advanced Explainability:** Implement SHAP or LIME to highlight exactly which words triggered the phishing classification.
- **Continuous Learning & Cloud Deployment:** Set up a feedback loop for misclassified emails and containerize the application for cloud deployment.

## 34. Security Considerations
- **No URL Execution:** URLs are parsed as plain text and never automatically visited or executed by the backend.
- **Data Privacy:** Email contents submitted to the API are processed in memory and are not permanently stored or unnecessarily logged.
- **API Security:** Stack traces and internal model paths are masked from API responses.
- **Production Enhancements:** Future deployments should include strict CORS, rate limiting, and authentication.

## 35. Conclusion
This project successfully demonstrates the integration of a deep learning NLP model (BERT) with heuristic security analysis (URL features) into a cohesive, user-friendly cybersecurity product. Despite the false-positive limitations inherent in aggressive threat modeling, the system achieves excellent recall and provides a solid foundation for robust email phishing defense.
