import pandas as pd

dataset_path = 'data/processed/email_phishing_dataset.csv'
df = pd.read_csv(dataset_path, low_memory=False)

# 1. Missing Values
total = len(df)
missing_subj = df['subject'].isna().sum()
empty_subj = (df['subject'] == '').sum()
missing_body = df['body'].isna().sum()
empty_body = (df['body'] == '').sum()
missing_label = df['label'].isna().sum()

missing_total = df.isna().sum().sum()

print("--- MISSING VALUES ---")
print(f"Missing subject: {missing_subj} (Null) + {empty_subj} (Empty string)")
print(f"Missing body: {missing_body} (Null) + {empty_body} (Empty string)")
print(f"Missing total: {missing_total}")
print(f"Number of emails affected: {df.isna().any(axis=1).sum()}")

# 2. HTML Detection
# In Phase 1 `clean.py`, we explicitly ran:
# text = html.unescape(text)
# text = re.sub(r'<[^>]+>', ' ', text)
# This removed HTML tags from all subjects and bodies before saving to intermediate/processed.

# 3. Final Validation
print("--- FINAL VALIDATION ---")
print(f"Total emails: {total}")
legit = len(df[df['label'].astype(str) == '0'])
phish = len(df[df['label'].astype(str) == '1'])
print(f"Legitimate: {legit}")
print(f"Phishing: {phish}")
print(f"Duplicates: {df.duplicated(subset=['bert_text']).sum()}")
print(f"Invalid labels: {(~df['label'].astype(str).isin(['0', '1'])).sum()}")
