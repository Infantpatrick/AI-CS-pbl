import pandas as pd
from sklearn.model_selection import train_test_split
import os

dataset_path = 'data/processed/email_phishing_dataset.csv'
report_path = 'results/split_report.md'
out_dir = 'data/processed'

# 1. Load Dataset
print("Loading dataset...")
df = pd.read_csv(dataset_path, low_memory=False)

# Ensure label is string
df['label'] = df['label'].astype(str)

# Verify duplicates in subject + body
df['norm_text'] = (df['subject'].fillna('') + df['body'].fillna('')).str.lower().str.replace(r'\s+', '', regex=True)
duplicate_count = df.duplicated(subset=['norm_text']).sum()
if duplicate_count > 0:
    print(f"Warning: Found {duplicate_count} duplicates. Removing them to prevent data leakage...")
    df = df.drop_duplicates(subset=['norm_text']).copy()
else:
    print("No duplicates found. Data leakage check passed.")

df = df.drop(columns=['norm_text'])
total_records = len(df)

# 2. Train / Validation / Test Split
print("Splitting dataset...")
train_df, temp_df = train_test_split(df, test_size=0.20, stratify=df['label'], random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.50, stratify=temp_df['label'], random_state=42)

# Verify disjointness
train_idx = set(train_df.index)
val_idx = set(val_df.index)
test_idx = set(test_df.index)
overlap = len(train_idx & val_idx) + len(train_idx & test_idx) + len(val_idx & test_idx)

def get_stats(dataset):
    total = len(dataset)
    legit = len(dataset[dataset['label'] == '0'])
    phish = len(dataset[dataset['label'] == '1'])
    return total, legit, phish

total_train, legit_train, phish_train = get_stats(train_df)
total_val, legit_val, phish_val = get_stats(val_df)
total_test, legit_test, phish_test = get_stats(test_df)

# 4. Save the Splits
print("Saving splits...")
train_df.to_csv(os.path.join(out_dir, 'train.csv'), index=False)
val_df.to_csv(os.path.join(out_dir, 'validation.csv'), index=False)
test_df.to_csv(os.path.join(out_dir, 'test.csv'), index=False)

# 5. Create Report
print("Generating report...")
with open(report_path, 'w') as f:
    f.write(f"Total Dataset: {total_records}\n")
    f.write(f"Training: {total_train}\n")
    f.write(f"Validation: {total_val}\n")
    f.write(f"Testing: {total_test}\n\n")
    
    f.write("Training:\n")
    f.write(f"- Legitimate: {legit_train}\n")
    f.write(f"- Phishing: {phish_train}\n\n")
    
    f.write("Validation:\n")
    f.write(f"- Legitimate: {legit_val}\n")
    f.write(f"- Phishing: {phish_val}\n\n")
    
    f.write("Testing:\n")
    f.write(f"- Legitimate: {legit_test}\n")
    f.write(f"- Phishing: {phish_test}\n\n")
    
    f.write("Data Leakage:\n")
    f.write(f"Duplicate Records Across Splits: {overlap}\n")

summary = f"""PHASE 3 SUMMARY

Total Dataset: {total_records}
Training: {total_train}
Validation: {total_val}
Testing: {total_test}

Training:
- Legitimate: {legit_train}
- Phishing: {phish_train}

Validation:
- Legitimate: {legit_val}
- Phishing: {phish_val}

Testing:
- Legitimate: {legit_test}
- Phishing: {phish_test}

Data Leakage:
Duplicate Records Across Splits: {overlap}
"""
print("PHASE_3_DELIMITER")
print(summary)
