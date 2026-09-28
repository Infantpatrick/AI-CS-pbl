import os
import pandas as pd

proc_file = 'data/processed/email_phishing_dataset.csv'
map_file = 'data/label_mapping.csv'
report_file = 'data/LABEL_AUDIT_REPORT.md'

# Load label mapping
label_map = pd.read_csv(map_file)

# Load final dataset
df = pd.read_csv(proc_file, low_memory=False)

total_emails = len(df)
legitimate_count = len(df[df['label'].astype(str) == '0'])
phishing_count = len(df[df['label'].astype(str) == '1'])

sources_counts = df['source'].value_counts().to_dict()

# Missing Values in Final Dataset
missing_subj = df['subject'].isna().sum() + (df['subject'] == '').sum()
missing_body = df['body'].isna().sum() + (df['body'] == '').sum()
missing_label = df['label'].isna().sum()

# Duplicates in Final Dataset (bert_text)
exact_dups = df.duplicated(subset=['bert_text']).sum()

# Invalid labels
invalid_labels = df[~df['label'].astype(str).isin(['0', '1'])].shape[0]

# Potential Label Errors Logic
label_errors = []
for index, row in label_map.iterrows():
    dataset = str(row['Dataset']).lower()
    orig_label = str(row['Original Label']).lower()
    proposed = str(row['Proposed Standard Label'])
    
    # Check if spam is being mapped to phishing without distinction
    if 'spam' in dataset or orig_label == 'spam':
        if proposed == '1':
            label_errors.append(f"- **{row['Dataset']}**: Original label '{row['Original Label']}' (Spam) was mapped to '1' (Phishing). Spam is not always phishing.")
            
    # Check Enron
    if 'enron' in dataset and proposed == '1':
         label_errors.append(f"- **{row['Dataset']}**: Original label '{row['Original Label']}' was mapped to '1'. Ensure this specific Enron subset genuinely represents phishing rather than generic spam/malware.")
         
    # Check Ling
    if 'ling' in dataset and proposed == '1':
         label_errors.append(f"- **{row['Dataset']}**: Original label '{row['Original Label']}' was mapped to '1'. Ling-spam is a spam corpus, not strictly phishing.")

with open(report_file, 'w') as f:
    f.write("# LABEL AUDIT REPORT\n\n")
    
    f.write("## 1. Label Mapping Verification\n")
    f.write("Below is how each dataset's original labels were mapped:\n\n")
    f.write("| Dataset | Original Label | Standard Label | Meaning |\n")
    f.write("|---------|----------------|----------------|---------|\n")
    for index, row in label_map.iterrows():
        f.write(f"| {row['Dataset']} | {row['Original Label']} | {row['Proposed Standard Label']} | {row['Meaning']} |\n")
    
    f.write("\n## 2. Dataset Statistics\n")
    f.write(f"- **Total Emails**: {total_emails}\n")
    f.write(f"- **Legitimate Count (0)**: {legitimate_count}\n")
    f.write(f"- **Phishing Count (1)**: {phishing_count}\n\n")
    
    f.write("### Counts from Each Source\n")
    for src, count in sources_counts.items():
        f.write(f"- {src}: {count}\n")
        
    f.write("\n## 3. Data Quality in Final Dataset\n")
    f.write(f"- **Missing Subjects**: {missing_subj}\n")
    f.write(f"- **Missing Bodies**: {missing_body}\n")
    f.write(f"- **Missing Labels**: {missing_label}\n")
    f.write(f"- **Exact Duplicates (Remaining)**: {exact_dups}\n")
    f.write(f"- **Invalid Labels (Remaining)**: {invalid_labels}\n")
    
    f.write("\n## 4. Possible Label Errors / Ambiguities\n")
    if not label_errors:
        f.write("No obvious label ambiguities detected based on dataset names and labels.\n")
    else:
        for error in set(label_errors):
            f.write(f"{error}\n")

print("Audit complete.")
