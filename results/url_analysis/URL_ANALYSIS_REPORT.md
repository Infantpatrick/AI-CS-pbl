# URL ANALYSIS VERIFICATION REPORT

### Extraction Method
URLs are extracted using a robust regular expression that captures standard web links (http, https, www) while excluding surrounding punctuation.

### Features Analyzed
- Full URL, Domain, URL length, Domain length, HTTPS usage, HTTP usage, IP address domain, number of dots, number of subdomains, special characters count, query parameters count, presence of @ symbol, suspicious keywords, URL shortener patterns, and hexadecimal encoding.

### Suspicious Indicators Generated
- ip_address_used
- http_used
- excessive_subdomains (>2)
- excessive_url_length (>75)
- suspicious_keywords_found
- url_shortener
- contains_at_symbol
- excessive_special_chars (>15)
- suspicious_encoding

### Limitations
- Rule-based static analysis might flag legitimate long URLs or specific platforms as suspicious (false positives).
- Sophisticated attacks might avoid these specific patterns (false negatives).

### Security Considerations
- **Zero External Requests:** All analysis is performed statically using regex and string manipulation. The system does NOT resolve domains, send HTTP requests, or fetch any URL content, ensuring complete safety from malicious payloads or tracking pixels.

### Test Cases & Results
#### Test 1: Normal HTTPS URL - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "https://docs.google.com/document/d/12345/edit",
      "domain": "docs.google.com",
      "uses_https": true,
      "uses_http": false,
      "url_length": 45,
      "domain_length": 15,
      "is_ip": false,
      "num_dots": 2,
      "num_subdomains": 1,
      "num_special_chars": 7,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [],
      "indicator_count": 0
    }
  ]
}
```

#### Test 2: HTTP URL - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "http://myblog.com/post1",
      "domain": "myblog.com",
      "uses_https": false,
      "uses_http": true,
      "url_length": 23,
      "domain_length": 10,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 4,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [
        "http_used"
      ],
      "indicator_count": 1
    }
  ]
}
```

#### Test 3: IP-based URL - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "http://192.168.1.1:8080/admin",
      "domain": "192.168.1.1:8080",
      "uses_https": false,
      "uses_http": true,
      "url_length": 29,
      "domain_length": 16,
      "is_ip": true,
      "num_dots": 3,
      "num_subdomains": 0,
      "num_special_chars": 5,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [
        "admin"
      ],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [
        "ip_address_used",
        "http_used",
        "suspicious_keywords_found:admin"
      ],
      "indicator_count": 3
    }
  ]
}
```

#### Test 4: URL with suspicious keywords - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "https://paypal-secure-update-login.com",
      "domain": "paypal-secure-update-login.com",
      "uses_https": true,
      "uses_http": false,
      "url_length": 38,
      "domain_length": 30,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 3,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [
        "login",
        "update",
        "secure"
      ],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [
        "suspicious_keywords_found:login,update,secure"
      ],
      "indicator_count": 1
    }
  ]
}
```

#### Test 5: Very long URL - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "https://example.com/path/to/resource?data=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "domain": "example.com",
      "uses_https": true,
      "uses_http": false,
      "url_length": 122,
      "domain_length": 11,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 8,
      "num_query_params": 1,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [
        "excessive_url_length"
      ],
      "indicator_count": 1
    }
  ]
}
```

#### Test 6: URL with multiple query parameters - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "https://shop.com/search?q=shoes&sort=price&order=asc&page=2&ref=email",
      "domain": "shop.com",
      "uses_https": true,
      "uses_http": false,
      "url_length": 69,
      "domain_length": 8,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 14,
      "num_query_params": 5,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [],
      "indicator_count": 0
    }
  ]
}
```

#### Test 7: URL shortener pattern - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "https://bit.ly/3xYzQw1",
      "domain": "bit.ly",
      "uses_https": true,
      "uses_http": false,
      "url_length": 22,
      "domain_length": 6,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 4,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": true,
      "contains_encoded": false,
      "suspicious_indicators": [
        "url_shortener"
      ],
      "indicator_count": 1
    }
  ]
}
```

#### Test 8: Email containing multiple URLs - PASS
```json
{
  "urls_found": 3,
  "urls": [
    {
      "url": "https://cnn.com",
      "domain": "cnn.com",
      "uses_https": true,
      "uses_http": false,
      "url_length": 15,
      "domain_length": 7,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 3,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [],
      "indicator_count": 0
    },
    {
      "url": "https://bbc.co.uk",
      "domain": "bbc.co.uk",
      "uses_https": true,
      "uses_http": false,
      "url_length": 17,
      "domain_length": 9,
      "is_ip": false,
      "num_dots": 2,
      "num_subdomains": 1,
      "num_special_chars": 3,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [],
      "indicator_count": 0
    },
    {
      "url": "http://twitter.com/news",
      "domain": "twitter.com",
      "uses_https": false,
      "uses_http": true,
      "url_length": 23,
      "domain_length": 11,
      "is_ip": false,
      "num_dots": 1,
      "num_subdomains": 0,
      "num_special_chars": 4,
      "num_query_params": 0,
      "contains_at_symbol": false,
      "suspicious_keywords": [],
      "is_shortener": false,
      "contains_encoded": false,
      "suspicious_indicators": [
        "http_used"
      ],
      "indicator_count": 1
    }
  ]
}
```

#### Test 9: Email containing no URLs - PASS
```json
{
  "urls_found": 0,
  "urls": [],
  "message": "No URLs detected"
}
```

#### Test 10: Malformed/invalid URL input - PASS
```json
{
  "urls_found": 1,
  "urls": [
    {
      "url": "http://[invalid-ip]/",
      "domain": "unknown",
      "uses_https": false,
      "url_length": 20,
      "suspicious_indicators": [
        "malformed_url"
      ],
      "indicator_count": 1
    }
  ]
}
```

