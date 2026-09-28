import re
from urllib.parse import urlparse

# Suspicious keywords commonly found in phishing URLs
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm',
    'password', 'auth', 'signin', 'billing', 'support', 'service', 'validation',
    'admin', 'webmail', 'portal'
]

# Common URL shorteners
URL_SHORTENERS = [
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'is.gd', 'cli.gs',
    'yfrog.com', 'migre.me', 'ff.im', 'tiny.cc', 'url4.eu', 'twit.ac',
    'su.pr', 'twurl.nl', 'snipurl.com', 'short.to', 'BudURL.com', 'ping.fm',
    'post.ly', 'Just.as', 'bkite.com', 'snipr.com', 'fic.kr', 'loopt.us',
    'doiop.com', 'short.ie', 'kl.am', 'wp.me', 'rubyurl.com', 'om.ly',
    'to.ly', 'bit.do', 't2m.io', 'rebrandly.com', 'cutt.ly', 'cutt.us'
]

def extract_urls(text):
    """
    Extracts URLs from a given text.
    Handles http, https, and www prefixes.
    Removes duplicates while preserving order.
    """
    if not isinstance(text, str):
        return []
        
    # Regex to capture http, https, and www. URLs
    url_pattern = re.compile(r'(?i)\b(?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])')
    
    urls_found = []
    seen = set()
    
    for match in url_pattern.finditer(text):
        url = match.group(0)
        # Ensure it starts with http or https for parsing, if it only started with www.
        if not url.lower().startswith('http'):
            url = 'http://' + url
            
        if url not in seen:
            urls_found.append(url)
            seen.add(url)
            
    return urls_found

def analyze_url(url):
    """
    Statically analyzes a URL and calculates features and suspicious indicators.
    Does NOT make any network requests.
    """
    indicators = []
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
    except Exception:
        # Malformed URL
        return {
            "url": url,
            "domain": "unknown",
            "uses_https": False,
            "url_length": len(url),
            "suspicious_indicators": ["malformed_url"],
            "indicator_count": 1
        }
        
    # 1. Features
    url_length = len(url)
    domain_length = len(domain)
    uses_https = url.startswith('https://')
    uses_http = url.startswith('http://')
    
    # Check for IP address instead of domain
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$')
    is_ip = bool(ip_pattern.match(domain))
    
    num_dots = domain.count('.')
    num_subdomains = num_dots - 1 if num_dots > 0 and not is_ip else 0
    num_special_chars = len(re.findall(r'[^a-zA-Z0-9\-\.]', url))
    num_query_params = len(query.split('&')) if query else 0
    contains_at_symbol = '@' in url
    
    # Suspicious keywords in URL
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url.lower()]
    
    # URL shortener pattern
    is_shortener = any(shortener in domain.lower() for shortener in URL_SHORTENERS)
    
    # Encoded characters (hexadecimal percent encoding)
    contains_encoded = '%' in url
    
    # 2. Suspicious Indicators Generation
    if is_ip:
        indicators.append("ip_address_used")
    if uses_http:
        indicators.append("http_used")
    if num_subdomains > 2:
        indicators.append("excessive_subdomains")
    if url_length > 75:
        indicators.append("excessive_url_length")
    if found_keywords:
        indicators.append(f"suspicious_keywords_found:{','.join(found_keywords)}")
    if is_shortener:
        indicators.append("url_shortener")
    if contains_at_symbol:
        indicators.append("contains_at_symbol")
    if num_special_chars > 15:
        indicators.append("excessive_special_chars")
    if contains_encoded:
        indicators.append("suspicious_encoding")
        
    return {
        "url": url,
        "domain": domain,
        "uses_https": uses_https,
        "uses_http": uses_http,
        "url_length": url_length,
        "domain_length": domain_length,
        "is_ip": is_ip,
        "num_dots": num_dots,
        "num_subdomains": num_subdomains,
        "num_special_chars": num_special_chars,
        "num_query_params": num_query_params,
        "contains_at_symbol": contains_at_symbol,
        "suspicious_keywords": found_keywords,
        "is_shortener": is_shortener,
        "contains_encoded": contains_encoded,
        "suspicious_indicators": indicators,
        "indicator_count": len(indicators)
    }

def analyze_email_urls(subject, body):
    """
    Extracts and analyzes all URLs from an email subject and body.
    """
    text = f"{subject if subject else ''}\n{body if body else ''}"
    urls = extract_urls(text)
    
    if not urls:
        return {
            "urls_found": 0,
            "urls": [],
            "message": "No URLs detected"
        }
        
    analyzed_urls = [analyze_url(url) for url in urls]
    
    return {
        "urls_found": len(analyzed_urls),
        "urls": analyzed_urls
    }
