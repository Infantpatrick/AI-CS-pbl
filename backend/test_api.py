import os
import sys
import json
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app

client = TestClient(app)

def run_tests():
    print("Running Backend API Tests...\n")
    results = []

    # 1. GET /health
    print("Test 1: GET /health")
    response = client.get("/health")
    if response.status_code == 200 and response.json() == {"status": "healthy"}:
        print("PASS\n")
        results.append({"case": "GET /health", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "GET /health", "status": "FAIL", "error": response.text})

    # 2. GET /model-info
    print("Test 2: GET /model-info")
    response = client.get("/model-info")
    if response.status_code == 200 and "model" in response.json():
        print("PASS\n")
        results.append({"case": "GET /model-info", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "GET /model-info", "status": "FAIL", "error": response.text})

    # 3. POST /predict with legitimate email
    print("Test 3: POST /predict with legitimate email")
    payload = {"subject": "Meeting Notes", "body": "Please review the attached notes for tomorrow's meeting."}
    response = client.post("/predict", json=payload)
    if response.status_code == 200 and "risk_level" in response.json():
        print("PASS\n")
        results.append({"case": "Legitimate Email", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Legitimate Email", "status": "FAIL", "error": response.text})

    # 4. POST /predict with phishing email
    print("Test 4: POST /predict with phishing email")
    payload = {"subject": "URGENT: Your Account Has Been Compromised", "body": "Dear User, verify your identity here: http://secure-login-update.com"}
    response = client.post("/predict", json=payload)
    if response.status_code == 200:
        print("PASS\n")
        results.append({"case": "Phishing Email", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Phishing Email", "status": "FAIL", "error": response.text})

    # 5. POST /predict with suspicious URL
    print("Test 5: POST /predict with suspicious URL")
    payload = {"subject": "Update required", "body": "Go to http://192.168.1.1/admin to update."}
    response = client.post("/predict", json=payload)
    if response.status_code == 200:
        print("PASS\n")
        results.append({"case": "Suspicious URL", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Suspicious URL", "status": "FAIL", "error": response.text})

    # 6. POST /predict with no URL
    print("Test 6: POST /predict with no URL")
    payload = {"subject": "Hello", "body": "Just checking in, hope you are well."}
    response = client.post("/predict", json=payload)
    if response.status_code == 200:
        print("PASS\n")
        results.append({"case": "No URL", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "No URL", "status": "FAIL", "error": response.text})

    # 7. Empty input (Caught by validation)
    print("Test 7: Empty input")
    payload = {"subject": "", "body": ""}
    response = client.post("/predict", json=payload)
    if response.status_code in [400, 422]:
        print("PASS (Caught appropriately)\n")
        results.append({"case": "Empty Input", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Empty Input", "status": "FAIL", "error": response.text})

    # 8. Missing fields
    print("Test 8: Missing fields")
    payload = {"subject": "Hello"}
    response = client.post("/predict", json=payload)
    if response.status_code == 422:
        print("PASS (Validation error)\n")
        results.append({"case": "Missing fields", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Missing fields", "status": "FAIL", "error": response.text})

    # 9. Invalid input
    print("Test 9: Invalid input")
    payload = {"subject": ["Not a string"], "body": "Body"}
    response = client.post("/predict", json=payload)
    if response.status_code == 422:
        print("PASS (Validation error)\n")
        results.append({"case": "Invalid input", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Invalid input", "status": "FAIL", "error": response.text})

    # 10. Long email
    print("Test 10: Long email")
    payload = {"subject": "Details", "body": "A" * 5000}
    response = client.post("/predict", json=payload)
    if response.status_code == 200:
        print("PASS\n")
        results.append({"case": "Long email", "status": "PASS", "result": response.json()})
    else:
        print(f"FAIL: {response.text}\n")
        results.append({"case": "Long email", "status": "FAIL", "error": response.text})

    return results

if __name__ == "__main__":
    test_results = run_tests()
    
    # Save Report
    os.makedirs('results/backend', exist_ok=True)
    report_path = 'results/backend/BACKEND_API_REPORT.md'
    
    with open(report_path, 'w') as f:
        f.write("# BACKEND API VERIFICATION REPORT\n\n")
        
        f.write("### Architecture\n")
        f.write("FastAPI-based RESTful API serving the Phase 12 risk assessment module. It leverages Pydantic for schema validation, ensuring valid inputs before model inference.\n\n")
        
        f.write("### API Endpoints\n")
        f.write("- **GET `/health`**: Returns API status.\n")
        f.write("- **GET `/model-info`**: Returns basic metadata about the loaded BERT model.\n")
        f.write("- **POST `/predict`**: Processes email subject and body and returns risk assessment.\n\n")
        
        f.write("### Model Loading Approach\n")
        f.write("The fine-tuned BERT model and tokenizer are instantiated lazily on the first request (or module import in Phase 10 logic) and reused for all subsequent requests to avoid loading overhead per request.\n\n")
        
        f.write("### Validation Rules\n")
        f.write("- Subject and Body must be valid strings.\n")
        f.write("- Maximum input constraints enforced (1000 for subject, 50000 for body).\n")
        f.write("- At least one field (subject or body) must contain text (prevent empty evaluations).\n\n")

        f.write("### Test Cases & Results\n")
        for res in test_results:
            f.write(f"#### {res['case']} - {res['status']}\n")
            if 'result' in res:
                f.write(f"```json\n{json.dumps(res['result'], indent=2)}\n```\n")
            if 'error' in res:
                f.write(f"Error: {res['error']}\n")
            f.write("\n")
            
    print(f"Verification report saved to {report_path}")
