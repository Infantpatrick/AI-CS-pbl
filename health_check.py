import os
import sys
import json
import time
import subprocess
import requests
import pandas as pd
import torch

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def run_health_check():
    print("Running Complete Project Health Check...\n")
    results = {}
    errors = []

    # PHASE 1: DATASET
    try:
        if os.path.exists('data/processed/train.csv'):
            df = pd.read_csv('data/processed/train.csv', nrows=5)
            if 'label' in df.columns:
                results['Dataset'] = 'PASS'
            else:
                results['Dataset'] = 'FAIL'
                errors.append("Dataset missing label column")
        else:
            results['Dataset'] = 'FAIL'
            errors.append("Processed dataset not found")
    except Exception as e:
        results['Dataset'] = 'FAIL'
        errors.append(f"Dataset error: {e}")

    # PHASE 2: DATA SPLIT
    try:
        files = ['train.csv', 'validation.csv', 'test.csv']
        all_exist = all(os.path.exists(f'data/processed/{f}') for f in files)
        if all_exist:
            results['Data Split'] = 'PASS'
        else:
            results['Data Split'] = 'FAIL'
            errors.append("Data split files missing")
    except Exception as e:
        results['Data Split'] = 'FAIL'
        errors.append(f"Data split error: {e}")

    # PHASE 3: TOKENIZATION
    try:
        if os.path.exists('data/tokenized/train.npz'):
            results['Tokenization'] = 'PASS'
        else:
            results['Tokenization'] = 'FAIL'
            errors.append("Tokenized files missing in data/tokenized/")
    except Exception as e:
        results['Tokenization'] = 'FAIL'
        errors.append(f"Tokenization error: {e}")

    # PHASE 4: BERT MODEL
    try:
        model_dir = 'models/bert_phishing'
        if os.path.exists(os.path.join(model_dir, 'config.json')) and \
           (os.path.exists(os.path.join(model_dir, 'model.safetensors')) or os.path.exists(os.path.join(model_dir, 'pytorch_model.bin'))) and \
           os.path.exists(os.path.join(model_dir, 'tokenizer.json')):
            results['Fine-tuned BERT Model'] = 'PASS'
        else:
            results['Fine-tuned BERT Model'] = 'FAIL'
            errors.append("BERT model files missing in models/bert_phishing")
    except Exception as e:
        results['Fine-tuned BERT Model'] = 'FAIL'
        errors.append(f"BERT Model error: {e}")

    # PHASE 5: MODEL EVALUATION
    try:
        # It could be in results/evaluation or results/bert_evaluation
        if os.path.exists('results/evaluation/EVALUATION_REPORT.md') or os.path.exists('results/reports/BERT_EVALUATION_REPORT.md'):
            results['Model Evaluation'] = 'PASS'
        else:
            results['Model Evaluation'] = 'FAIL'
            errors.append("Evaluation report missing")
    except Exception as e:
        results['Model Evaluation'] = 'FAIL'
        errors.append(f"Evaluation error: {e}")

    # PHASE 6: ERROR ANALYSIS
    try:
        if os.path.exists('results/error_analysis/ERROR_ANALYSIS_REPORT.md') or os.path.exists('results/reports/ERROR_ANALYSIS_REPORT.md'):
            results['Error Analysis'] = 'PASS'
        else:
            results['Error Analysis'] = 'FAIL'
            errors.append("Error analysis report missing")
    except Exception as e:
        results['Error Analysis'] = 'FAIL'
        errors.append(f"Error analysis error: {e}")

    # PHASE 7: PREDICTION PIPELINE
    try:
        from src.model.prediction_pipeline import predict_email
        res = predict_email("Subject", "Body")
        if "prediction" in res:
            results['Prediction Pipeline'] = 'PASS'
        else:
            results['Prediction Pipeline'] = 'FAIL'
            errors.append("Prediction pipeline returned invalid format")
    except Exception as e:
        results['Prediction Pipeline'] = 'FAIL'
        errors.append(f"Prediction Pipeline error: {e}")

    # PHASE 8: URL ANALYSIS
    try:
        from src.utils.url_analyzer import analyze_email_urls
        res = analyze_email_urls("Subject", "http://google.com")
        if "urls_found" in res:
            results['URL Analysis'] = 'PASS'
        else:
            results['URL Analysis'] = 'FAIL'
            errors.append("URL Analysis returned invalid format")
    except Exception as e:
        results['URL Analysis'] = 'FAIL'
        errors.append(f"URL Analysis error: {e}")

    # PHASE 9: RISK ASSESSMENT
    try:
        from src.model.risk_assessment import assess_email_risk
        res = assess_email_risk("Subject", "Body")
        if "risk_level" in res:
            results['Risk Assessment'] = 'PASS'
        else:
            results['Risk Assessment'] = 'FAIL'
            errors.append("Risk Assessment returned invalid format")
    except Exception as e:
        results['Risk Assessment'] = 'FAIL'
        errors.append(f"Risk Assessment error: {e}")

    # PHASE 10: BACKEND API (LIVE SERVER TEST)
    print("Starting FastAPI backend server...")
    process = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app:app", "--port", "8000"], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server to start with a retry loop
    server_ready = False
    for _ in range(30):
        try:
            resp = requests.get(f"{base_url}/health")
            if resp.status_code == 200:
                server_ready = True
                break
        except Exception:
            time.sleep(1)
            
    if not server_ready:
        errors.append("Backend server failed to start within 30 seconds.")
    
    # Defaults to FAIL, set to PASS if successful
    results['Backend API'] = 'FAIL'
    results['API /health'] = 'FAIL'
    results['API /model-info'] = 'FAIL'
    results['API /predict'] = 'FAIL'
    results['API Validation'] = 'FAIL'
    results['Swagger /docs'] = 'FAIL'
    results['ReDoc /redoc'] = 'FAIL'

    backend_ok = server_ready
    try:
        if server_ready:
            # /health
            resp = requests.get(f"{base_url}/health")
            if resp.status_code == 200 and resp.json().get("status") == "healthy":
                results['API /health'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/health failed: {resp.status_code}")

            # /model-info
            resp = requests.get(f"{base_url}/model-info")
            if resp.status_code == 200 and "model" in resp.json():
                results['API /model-info'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/model-info failed: {resp.status_code}")

            # /predict Legitimate
            resp = requests.post(f"{base_url}/predict", json={"subject": "Hello", "body": "Just checking in."})
            if resp.status_code == 200 and "risk_level" in resp.json():
                results['API /predict'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/predict Legitimate failed: {resp.status_code}")
                
            # /predict Validation (Empty)
            resp = requests.post(f"{base_url}/predict", json={"subject": "", "body": ""})
            if resp.status_code in [400, 422]:
                results['API Validation'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/predict validation failed: expected 400/422, got {resp.status_code}")

            # /docs
            resp = requests.get(f"{base_url}/docs")
            if resp.status_code == 200 and "swagger-ui" in resp.text.lower():
                results['Swagger /docs'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/docs failed: {resp.status_code}")

            # /redoc
            resp = requests.get(f"{base_url}/redoc")
            if resp.status_code == 200 and "redoc" in resp.text.lower():
                results['ReDoc /redoc'] = 'PASS'
            else:
                backend_ok = False
                errors.append(f"/redoc failed: {resp.status_code}")
                
            if backend_ok:
                results['Backend API'] = 'PASS'
            
    except Exception as e:
        errors.append(f"Backend Server communication error: {e}")
    finally:
        print("Stopping backend server...")
        process.terminate()
        process.wait()

    # Create Report
    os.makedirs('results/project_health_check', exist_ok=True)
    report_path = 'results/project_health_check/PROJECT_HEALTH_CHECK_REPORT.md'
    
    with open(report_path, 'w') as f:
        f.write("# PROJECT HEALTH CHECK REPORT\n\n")
        
        f.write("| Component | Status |\n")
        f.write("|---|---|\n")
        
        ordered_keys = [
            'Dataset', 'Data Split', 'Tokenization', 'Fine-tuned BERT Model',
            'Model Evaluation', 'Error Analysis', 'Prediction Pipeline',
            'URL Analysis', 'Risk Assessment', 'Backend API',
            'API /health', 'API /model-info', 'API /predict',
            'API Validation', 'Swagger /docs', 'ReDoc /redoc'
        ]
        
        for key in ordered_keys:
            status = results.get(key, 'FAIL')
            f.write(f"| {key} | {status} |\n")
            
        if errors:
            f.write("\n### Errors Found\n")
            for err in errors:
                f.write(f"- {err}\n")

    # Final Output
    print("\n========================================")
    print("PROJECT HEALTH CHECK")
    print("========================================")
    
    all_pass = all(v == 'PASS' for v in results.values())
    overall = 'PASS' if all_pass and not errors else 'FAIL'
    
    backend_keys = ['Backend API', 'API /health', 'API /model-info', 'API /predict', 'API Validation', 'Swagger /docs', 'ReDoc /redoc']
    backend_pass = all(results.get(k) == 'PASS' for k in backend_keys)
    backend_overall = 'PASS' if backend_pass else 'FAIL'
    
    print(f"\nOVERALL STATUS: {overall}")
    print(f"BACKEND STATUS: {backend_overall}")
    print(f"TOTAL ERRORS: {len(errors)}")
    
    if not all_pass:
        print("\nErrors identified:")
        for e in errors:
            print(f"- {e}")
            
    if all_pass:
        print("\nPROJECT READY FOR FRONTEND")

if __name__ == "__main__":
    run_health_check()
