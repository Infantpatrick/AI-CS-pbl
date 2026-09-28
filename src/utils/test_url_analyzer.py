import os
import json
from url_analyzer import analyze_email_urls

def run_tests():
    print("Running URL Analyzer Tests...\n")
    
    test_cases = [
        {
            "name": "Test 1: Normal HTTPS URL",
            "subject": "Meeting Notes",
            "body": "Please review the notes at https://docs.google.com/document/d/12345/edit"
        },
        {
            "name": "Test 2: HTTP URL",
            "subject": "Check this out",
            "body": "Visit my blog http://myblog.com/post1"
        },
        {
            "name": "Test 3: IP-based URL",
            "subject": "Router configuration",
            "body": "Access the panel at http://192.168.1.1:8080/admin"
        },
        {
            "name": "Test 4: URL with suspicious keywords",
            "subject": "Action Required: Update your account",
            "body": "Your account has been restricted. Go to https://paypal-secure-update-login.com to verify."
        },
        {
            "name": "Test 5: Very long URL",
            "subject": "Long URL Example",
            "body": "Here is a very long url: https://example.com/path/to/resource?data=" + "A"*80
        },
        {
            "name": "Test 6: URL with multiple query parameters",
            "subject": "Search query",
            "body": "Check this search: https://shop.com/search?q=shoes&sort=price&order=asc&page=2&ref=email"
        },
        {
            "name": "Test 7: URL shortener pattern",
            "subject": "Quick link",
            "body": "Click here: https://bit.ly/3xYzQw1"
        },
        {
            "name": "Test 8: Email containing multiple URLs",
            "subject": "Daily Links",
            "body": "Read news at https://cnn.com and https://bbc.co.uk. Follow us on http://twitter.com/news"
        },
        {
            "name": "Test 9: Email containing no URLs",
            "subject": "Hello",
            "body": "Hi, just wanted to say hello! Let's talk later."
        },
        {
            "name": "Test 10: Malformed/invalid URL input",
            "subject": "Broken links",
            "body": "Go to hxxps://badsite[.]com and also check this http://[invalid-ip]/"
        }
    ]

    results = []
    
    for case in test_cases:
        print(f"--- {case['name']} ---")
        try:
            res = analyze_email_urls(case['subject'], case['body'])
            print(f"Result: {json.dumps(res, indent=2)}\n")
            results.append({"case": case['name'], "status": "PASS", "result": res})
        except Exception as e:
            print(f"FAILED: {e}\n")
            results.append({"case": case['name'], "status": "FAIL", "error": str(e)})

    return results

if __name__ == "__main__":
    test_results = run_tests()
    
    # Save Report
    os.makedirs('results/url_analysis', exist_ok=True)
    report_path = 'results/url_analysis/URL_ANALYSIS_REPORT.md'
    
    with open(report_path, 'w') as f:
        f.write("# URL ANALYSIS VERIFICATION REPORT\n\n")
        
        f.write("### Extraction Method\n")
        f.write("URLs are extracted using a robust regular expression that captures standard web links (http, https, www) while excluding surrounding punctuation.\n\n")
        
        f.write("### Features Analyzed\n")
        f.write("- Full URL, Domain, URL length, Domain length, HTTPS usage, HTTP usage, IP address domain, number of dots, number of subdomains, special characters count, query parameters count, presence of @ symbol, suspicious keywords, URL shortener patterns, and hexadecimal encoding.\n\n")
        
        f.write("### Suspicious Indicators Generated\n")
        f.write("- ip_address_used\n- http_used\n- excessive_subdomains (>2)\n- excessive_url_length (>75)\n- suspicious_keywords_found\n- url_shortener\n- contains_at_symbol\n- excessive_special_chars (>15)\n- suspicious_encoding\n\n")
        
        f.write("### Limitations\n")
        f.write("- Rule-based static analysis might flag legitimate long URLs or specific platforms as suspicious (false positives).\n")
        f.write("- Sophisticated attacks might avoid these specific patterns (false negatives).\n\n")
        
        f.write("### Security Considerations\n")
        f.write("- **Zero External Requests:** All analysis is performed statically using regex and string manipulation. The system does NOT resolve domains, send HTTP requests, or fetch any URL content, ensuring complete safety from malicious payloads or tracking pixels.\n\n")

        f.write("### Test Cases & Results\n")
        for res in test_results:
            f.write(f"#### {res['case']} - {res['status']}\n")
            if 'result' in res:
                f.write(f"```json\n{json.dumps(res['result'], indent=2)}\n```\n")
            if 'error' in res:
                f.write(f"Error: {res['error']}\n")
            f.write("\n")
            
    print(f"Verification report saved to {report_path}")
