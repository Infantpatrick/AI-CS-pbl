export const getAppClassification = (riskLevel) => {
  if (!riskLevel) return 'UNKNOWN';
  const risk = riskLevel.toUpperCase();
  if (risk === 'HIGH' || risk === 'CRITICAL') return 'PHISHING';
  if (risk === 'MEDIUM') return 'SPAM';
  if (risk === 'LOW') return 'LEGITIMATE';
  return 'UNKNOWN';
};

export const normalizeRiskResponse = (data) => {
  const riskLevel = (data.risk_level || 'UNKNOWN').toUpperCase();
  return {
    prediction: (data.prediction || 'UNKNOWN').toUpperCase(),
    appClassification: getAppClassification(riskLevel),
    phishingProbability: typeof data.phishing_probability === 'number' ? data.phishing_probability : 0,
    legitimateProbability: typeof data.legitimate_probability === 'number' ? data.legitimate_probability : 0,
    confidence: typeof data.confidence === 'number' ? data.confidence : 0,
    riskLevel: riskLevel,
    urlsFound: typeof data.urls_found === 'number' ? data.urls_found : 0,
    extractedUrls: Array.isArray(data.extracted_urls) ? data.extracted_urls : [],
    urlIndicators: Array.isArray(data.url_indicators) ? data.url_indicators : [],
    riskReasons: Array.isArray(data.risk_reasons) ? data.risk_reasons : []
  };
};
