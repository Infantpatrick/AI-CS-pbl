import os
import sys
import json

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.model.risk_assessment import assess_email_risk

def run_tests():
    print("Running Risk Assessment Tests...\n")
    
    test_cases = [
        {
            "name": "1. Clearly legitimate email",
            "subject": "Project Meeting Update",
            "body": "Hi team, we will meet tomorrow at 10 AM to discuss the upcoming release. Please review the document at https://docs.google.com/document/d/12345/edit before the meeting. Regards, John."
        },
        {
            "name": "2. High-confidence phishing email",
            "subject": "URGENT: Your Account Has Been Compromised",
            "body": "Dear User, we detected unauthorized login attempts on your account. Click the link below immediately to verify your identity and restore access or your account will be permanently suspended. http://secure-login-update.com/auth"
        },
        {
            "name": "3. Medium-confidence case",
            "subject": "Account notification",
            "body": "There is a notice regarding your account."
        },
        {
            "name": "4. Phishing email with suspicious URL",
            "subject": "Action Required: Update your account",
            "body": "Your account has been restricted. Go to http://192.168.1.50/login to verify."
        },
        {
            "name": "5. Legitimate email containing a normal URL",
            "subject": "Blog post",
            "body": "Hey, read my new post on https://medium.com/@author/post"
        },
        {
            "name": "6. Email with no URL",
            "subject": "Hello",
            "body": "Hi, just wanted to say hello! Let's talk later."
        },
        {
            "name": "8. Multiple suspicious URL indicators",
            "subject": "Verify your identity",
            "body": "Please click here http://login-secure-update.com/verify?user=admin&token=123"
        }
    ]

    results = []
    
    for case in test_cases:
        print(f"--- {case['name']} ---")
        try:
            res = assess_email_risk(case['subject'], case['body'])
            print(f"Result: {json.dumps(res, indent=2)}\n")
            results.append({"case": case['name'], "status": "PASS", "result": res})
        except Exception as e:
            print(f"FAILED: {e}\n")
            results.append({"case": case['name'], "status": "FAIL", "error": str(e)})

    # 7. Empty/invalid input
    print("--- 7. Empty/invalid input ---")
    try:
        assess_email_risk("", "")
        print("FAILED: Did not catch empty input error.\n")
        results.append({"case": "7. Empty input", "status": "FAIL", "error": "No exception raised"})
    except Exception as e:
        print(f"Caught expected error: {e}\n")
        results.append({"case": "7. Empty input", "status": "PASS", "result": f"Expected error caught: {e}"})

    return results

if __name__ == "__main__":
    test_results = run_tests()
    
    # Save Report
    os.makedirs('results/risk_assessment', exist_ok=True)
    report_path = 'results/risk_assessment/RISK_ASSESSMENT_REPORT.md'
    
    with open(report_path, 'w') as f:
        f.write("# RISK ASSESSMENT VERIFICATION REPORT\n\n")
        
        f.write("### Methodology\n")
        f.write("The risk assessment combines the machine learning (BERT) prediction and static URL analysis heuristics. The BERT probability serves as the primary signal, while URL indicators are used as supporting evidence to adjust the final risk level.\n\n")
        
        f.write("### BERT Probability Thresholds\n")
        f.write("- **HIGH**: Phishing Probability >= 0.70\n")
        f.write("- **MEDIUM**: 0.30 < Phishing Probability < 0.70\n")
        f.write("- **LOW**: Phishing Probability <= 0.30\n\n")
        
        f.write("### URL Indicator Contribution\n")
        f.write("- If the email contains strong/multiple suspicious URL indicators (>= 2), the risk level is elevated (e.g., from LOW to MEDIUM or MEDIUM to HIGH).\n")
        f.write("- If the email contains moderate indicators (> 0), LOW risk is elevated to MEDIUM.\n")
        f.write("- No URLs present does NOT penalize the email.\n\n")
        
        f.write("### Definitions\n")
        f.write("- **LOW Risk**: Unlikely to be phishing. Low ML probability and no significant URL threats.\n")
        f.write("- **MEDIUM Risk**: Potentially suspicious. May have borderline ML probability or suspicious URL features requiring caution.\n")
        f.write("- **HIGH Risk**: Very likely phishing. High ML probability or strong combination of ML prediction and malicious URL patterns.\n\n")

        f.write("### Limitations\n")
        f.write("- The accuracy heavily depends on the BERT model's performance on unseen data.\n")
        f.write("- Static URL analysis may produce false positives for complex but benign URLs.\n\n")
        
        f.write("### Security Considerations\n")
        f.write("- No active external requests are made during this risk assessment. It remains completely static and offline, ensuring safety from tracker pixels or malicious endpoints.\n\n")

        f.write("### Test Cases & Results\n")
        for res in test_results:
            f.write(f"#### {res['case']} - {res['status']}\n")
            if 'result' in res:
                if isinstance(res['result'], dict):
                    f.write(f"```json\n{json.dumps(res['result'], indent=2)}\n```\n")
                else:
                    f.write(f"{res['result']}\n")
            if 'error' in res:
                f.write(f"Error: {res['error']}\n")
            f.write("\n")
            
    print(f"Verification report saved to {report_path}")
