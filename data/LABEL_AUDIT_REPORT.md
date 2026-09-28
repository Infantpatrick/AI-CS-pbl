# LABEL AUDIT REPORT

## 1. Label Mapping Verification
Below is how each dataset's original labels were mapped:

| Dataset | Original Label | Standard Label | Meaning |
|---------|----------------|----------------|---------|
| CEAS_08 | 1 | 1 | Phishing/Spam/Fraud |
| CEAS_08 | 0 | 0 | Legitimate |
| Enron | 0 | 0 | Legitimate |
| Enron | 1 | 1 | Phishing/Spam/Fraud |
| Ling | 0 | 0 | Legitimate |
| Ling | 1 | 1 | Phishing/Spam/Fraud |
| Nazario | 1 | 1 | Phishing/Spam/Fraud |
| Nigerian_Fraud | 1 | 1 | Phishing/Spam/Fraud |
| Phishing_Email | Safe Email | 0 | Legitimate |
| Phishing_Email | Phishing Email | 1 | Phishing/Spam/Fraud |
| SpamAssasin | 0 | 0 | Legitimate |
| SpamAssasin | 1 | 1 | Phishing/Spam/Fraud |

## 2. Dataset Statistics
- **Total Emails**: 87886
- **Legitimate Count (0)**: 43459
- **Phishing Count (1)**: 44427

### Counts from Each Source
- ceas: 38963
- enron: 29423
- other: 6134
- spamassassin: 5672
- nigerian_fraud: 3284
- ling_spam: 2859
- nazario: 1551

## 3. Data Quality in Final Dataset
- **Missing Subjects**: 6474
- **Missing Bodies**: 6
- **Missing Labels**: 0
- **Exact Duplicates (Remaining)**: 0
- **Invalid Labels (Remaining)**: 0

## 4. Possible Label Errors / Ambiguities
- **Ling**: Original label '1' was mapped to '1'. Ling-spam is a spam corpus, not strictly phishing.
- **Enron**: Original label '1' was mapped to '1'. Ensure this specific Enron subset genuinely represents phishing rather than generic spam/malware.
- **SpamAssasin**: Original label '1' (Spam) was mapped to '1' (Phishing). Spam is not always phishing.
