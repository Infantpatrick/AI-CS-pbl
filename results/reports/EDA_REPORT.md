# EXPLORATORY DATA ANALYSIS (EDA) REPORT

## Dataset Overview
- Total records: 87886
- Columns: 7 (email_id, subject, body, bert_text, label, source, original_label)
- Dataset size: 327.85 MB

## Class Analysis
- Legitimate count: 43459 (49.45%)
- Phishing count: 44427 (50.55%)

## Source Analysis
Records from each source:
- ceas: 38963 (44.33%)
- enron: 29423 (33.48%)
- other: 6134 (6.98%)
- spamassassin: 5672 (6.45%)
- nigerian_fraud: 3284 (3.74%)
- ling_spam: 2859 (3.25%)
- nazario: 1551 (1.76%)

Source vs Class Distribution:
| Source | Legitimate (0) | Phishing (1) | Total |
|--------|----------------|--------------|-------|
| ceas | 17289 | 21674 | 38963 |
| enron | 15474 | 13949 | 29423 |
| ling_spam | 2401 | 458 | 2859 |
| nazario | 0 | 1551 | 1551 |
| nigerian_fraud | 0 | 3284 | 3284 |
| other | 4209 | 1925 | 6134 |
| spamassassin | 4086 | 1586 | 5672 |

## Text Analysis
### Subject Statistics
- Average Length: 33.58 chars
### Body Statistics
- Average Length: 1879.34 chars
### Word Count Statistics
- Average Word Count: 313.57 words

### Most Frequent Words (Legitimate)
- http: 81308
- com: 78008
- have: 65247
- will: 60736
- submission: 54463
- enron: 52997
- can: 42932
- but: 41138
- all: 39661
- www: 39493
### Most Frequent Words (Phishing)
- com: 151094
- cnn: 114845
- http: 97902
- www: 79129
- html: 67705
- video: 60713
- index: 60071
- email: 54470
- will: 40150
- have: 38701

## Security-Related Analysis
- Emails containing URLs: 35952 (40.91%)
- Emails containing HTML: 0 (0.00%)

## Data Quality
- Missing values: 6480
- Duplicates (exact): 0
- Duplicates (norm): 0
- Invalid labels: 0

### Outliers (IQR Method)
- Short Subject Outliers: 0
- Long Subject Outliers: 2069
- Short Body Outliers: 0
- Long Body Outliers: 5880

## Key Findings
1. The dataset contains 87886 total emails.
2. Phishing emails represent 50.55% of the dataset, providing a highly balanced natural distribution.
3. Source 'ceas' contributes the largest number of emails (38963), while 'nazario' contributes the least (1551).
4. The average word count across all emails is 313.57 words.
5. A significant portion of emails contain URLs (35952 emails) and HTML (0 emails), which are common features analyzed in phishing detection.


## Phase 2.5: EDA Validation

### 1. Missing Values Analysis
The 6,480 total missing values are distributed as follows:
- **Subject**: 6,474 missing values (7.37%)
- **Body**: 6 missing values (0.01%)
- **Total Emails Affected**: 6,479 emails

### 2. HTML Detection
The EDA reported **0 HTML emails** because HTML tags were proactively removed during the Phase 1 cleaning process. The `clean.py` script utilized `html.unescape` and regex (`<[^>]+>`) to strip all tags like `<html>`, `<body>`, `<a>`, and `<table>` from the subjects and bodies before the dataset was saved to `data/processed/`.

### 3. Final Validation
- **Total emails**: 87,886
- **Legitimate**: 43,459
- **Phishing**: 44,427
- **Duplicates**: 0
- **Invalid labels**: 0
