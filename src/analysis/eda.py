import os
import re
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter 

# Set output directories
eda_dir = 'results/eda'
os.makedirs(eda_dir, exist_ok=True)
report_path = 'results/EDA_REPORT.md'
dataset_path = 'data/processed/email_phishing_dataset.csv'

# Load dataset
print("Loading dataset...")
df = pd.read_csv(dataset_path, low_memory=False)

# Make sure label is string/int standardized
df['label'] = df['label'].astype(str)

# Dataset Overview
total_emails = len(df)
num_columns = len(df.columns)
column_names = list(df.columns)
dataset_size = os.path.getsize(dataset_path) / (1024 * 1024)

# Data Quality
missing_values = df.isna().sum().sum()
empty_subjects = (df['subject'].fillna('') == '').sum()
empty_bodies = (df['body'].fillna('') == '').sum()
exact_duplicates = df.duplicated(subset=['bert_text']).sum()
norm_duplicates = df.duplicated(subset=['subject', 'body']).sum()
invalid_labels = (~df['label'].isin(['0', '1'])).sum()

# Clean missing values for text analysis
df['subject'] = df['subject'].fillna('').astype(str)
df['body'] = df['body'].fillna('').astype(str)

# Basic text stats
df['subject_len'] = df['subject'].apply(len)
df['body_len'] = df['body'].apply(len)
df['subject_words'] = df['subject'].apply(lambda x: len(x.split()))
df['body_words'] = df['body'].apply(lambda x: len(x.split()))
df['total_len'] = df['subject_len'] + df['body_len']
df['total_words'] = df['subject_words'] + df['body_words']

# Class Distribution
legit_df = df[df['label'] == '0']
phish_df = df[df['label'] == '1']
total_legit = len(legit_df)
total_phish = len(phish_df)
pct_legit = (total_legit / total_emails) * 100 if total_emails > 0 else 0
pct_phish = (total_phish / total_emails) * 100 if total_emails > 0 else 0

# Class Plot
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='label', palette='Set2')
plt.title('Class Distribution (0 = Legitimate, 1 = Phishing)')
plt.savefig(os.path.join(eda_dir, 'class_distribution.png'))
plt.close()

# Source Analysis
source_counts = df['source'].value_counts()
largest_source = source_counts.idxmax() if not source_counts.empty else "N/A"
smallest_source = source_counts.idxmin() if not source_counts.empty else "N/A"

plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='source', order=df['source'].value_counts().index, palette='viridis')
plt.title('Source Distribution')
plt.savefig(os.path.join(eda_dir, 'source_distribution.png'))
plt.close()

# Source x Class Plot
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='source', hue='label', palette='Set2')
plt.title('Source vs Class')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(eda_dir, 'source_vs_class.png'))
plt.close()

# Subject Analysis
avg_subj_len = df['subject_len'].mean()
avg_body_len = df['body_len'].mean()
avg_word_count = df['total_words'].mean()

plt.figure(figsize=(10, 6))
sns.histplot(data=df[df['subject_len'] < 200], x='subject_len', hue='label', bins=50, kde=True, palette='Set2')
plt.title('Subject Length Distribution (Truncated at 200 chars)')
plt.savefig(os.path.join(eda_dir, 'subject_length_distribution.png'))
plt.close()

# Body Analysis
plt.figure(figsize=(10, 6))
sns.histplot(data=df[df['body_len'] < 5000], x='body_len', hue='label', bins=50, kde=True, palette='Set2')
plt.title('Email Body Length Distribution (Truncated at 5000 chars)')
plt.savefig(os.path.join(eda_dir, 'email_length_distribution.png'))
plt.close()

# Word Count Analysis
plt.figure(figsize=(10, 6))
sns.histplot(data=df[df['total_words'] < 1000], x='total_words', hue='label', bins=50, kde=True, palette='Set2')
plt.title('Word Count Distribution (Truncated at 1000 words)')
plt.savefig(os.path.join(eda_dir, 'word_count_distribution.png'))
plt.close()

# Text Statistics & Frequent Words
stopwords = set(["the","to","and","of","a","in","for","is","on","that","by","this","with","i","you","it","not","or","be","are","from","at","as","your"])

def get_top_words(text_series, n=10):
    all_words = " ".join(text_series).lower()
    words = re.findall(r'\b[a-z]{3,}\b', all_words)
    words = [w for w in words if w not in stopwords]
    return Counter(words).most_common(n)

print("Calculating top words...")
top_words_legit = get_top_words(legit_df['subject'] + " " + legit_df['body'])
top_words_phish = get_top_words(phish_df['subject'] + " " + phish_df['body'])

# URL and HTML Analysis
df['has_url'] = df['body'].apply(lambda x: 1 if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(x)) else 0)
df['has_html'] = df['body'].apply(lambda x: 1 if re.search(r'<\s*[a-z][^>]*>', str(x).lower()) else 0)

emails_with_urls = df['has_url'].sum()
emails_with_html = df['has_html'].sum()

# URL presence by class
url_summary = df.groupby('label')['has_url'].mean() * 100
plt.figure(figsize=(6, 4))
url_summary.plot(kind='bar', color=['#4C72B0', '#DD8452'])
plt.title('Percentage of Emails with URLs by Class')
plt.ylabel('Percentage (%)')
plt.savefig(os.path.join(eda_dir, 'url_presence_by_class.png'))
plt.close()

# HTML presence by class
html_summary = df.groupby('label')['has_html'].mean() * 100
plt.figure(figsize=(6, 4))
html_summary.plot(kind='bar', color=['#4C72B0', '#DD8452'])
plt.title('Percentage of Emails with HTML by Class')
plt.ylabel('Percentage (%)')
plt.savefig(os.path.join(eda_dir, 'html_presence_by_class.png'))
plt.close()

# Outliers
Q1_subj = df['subject_len'].quantile(0.25)
Q3_subj = df['subject_len'].quantile(0.75)
IQR_subj = Q3_subj - Q1_subj
short_subj_outliers = (df['subject_len'] < (Q1_subj - 1.5 * IQR_subj)).sum()
long_subj_outliers = (df['subject_len'] > (Q3_subj + 1.5 * IQR_subj)).sum()

Q1_body = df['body_len'].quantile(0.25)
Q3_body = df['body_len'].quantile(0.75)
IQR_body = Q3_body - Q1_body
short_body_outliers = (df['body_len'] < (Q1_body - 1.5 * IQR_body)).sum()
long_body_outliers = (df['body_len'] > (Q3_body + 1.5 * IQR_body)).sum()

outliers_text = f"""- Short Subject Outliers: {short_subj_outliers}
- Long Subject Outliers: {long_subj_outliers}
- Short Body Outliers: {short_body_outliers}
- Long Body Outliers: {long_body_outliers}"""

# Generate Markdown Report
print("Generating markdown report...")
with open(report_path, 'w') as f:
    f.write("# EXPLORATORY DATA ANALYSIS (EDA) REPORT\n\n")
    
    f.write("## Dataset Overview\n")
    f.write(f"- Total records: {total_emails}\n")
    f.write(f"- Columns: {num_columns} ({', '.join(column_names)})\n")
    f.write(f"- Dataset size: {dataset_size:.2f} MB\n\n")
    
    f.write("## Class Analysis\n")
    f.write(f"- Legitimate count: {total_legit} ({pct_legit:.2f}%)\n")
    f.write(f"- Phishing count: {total_phish} ({pct_phish:.2f}%)\n\n")
    
    f.write("## Source Analysis\n")
    f.write("Records from each source:\n")
    for src, count in source_counts.items():
        f.write(f"- {src}: {count} ({count/total_emails*100:.2f}%)\n")
        
    f.write("\nSource vs Class Distribution:\n")
    src_class = df.groupby(['source', 'label']).size().unstack(fill_value=0)
    f.write("| Source | Legitimate (0) | Phishing (1) | Total |\n")
    f.write("|--------|----------------|--------------|-------|\n")
    for src in src_class.index:
        leg = src_class.loc[src, '0'] if '0' in src_class.columns else 0
        phi = src_class.loc[src, '1'] if '1' in src_class.columns else 0
        f.write(f"| {src} | {leg} | {phi} | {leg + phi} |\n")
    
    f.write("\n## Text Analysis\n")
    f.write("### Subject Statistics\n")
    f.write(f"- Average Length: {avg_subj_len:.2f} chars\n")
    f.write("### Body Statistics\n")
    f.write(f"- Average Length: {avg_body_len:.2f} chars\n")
    f.write("### Word Count Statistics\n")
    f.write(f"- Average Word Count: {avg_word_count:.2f} words\n\n")
    
    f.write("### Most Frequent Words (Legitimate)\n")
    for w, c in top_words_legit:
        f.write(f"- {w}: {c}\n")
    
    f.write("### Most Frequent Words (Phishing)\n")
    for w, c in top_words_phish:
        f.write(f"- {w}: {c}\n")
    
    f.write("\n## Security-Related Analysis\n")
    f.write(f"- Emails containing URLs: {emails_with_urls} ({(emails_with_urls/total_emails)*100:.2f}%)\n")
    f.write(f"- Emails containing HTML: {emails_with_html} ({(emails_with_html/total_emails)*100:.2f}%)\n\n")
    
    f.write("## Data Quality\n")
    f.write(f"- Missing values: {missing_values}\n")
    f.write(f"- Duplicates (exact): {exact_duplicates}\n")
    f.write(f"- Duplicates (norm): {norm_duplicates}\n")
    f.write(f"- Invalid labels: {invalid_labels}\n")
    f.write("\n### Outliers (IQR Method)\n")
    f.write(outliers_text + "\n\n")
    
    f.write("## Key Findings\n")
    f.write(f"1. The dataset contains {total_emails} total emails.\n")
    f.write(f"2. Phishing emails represent {pct_phish:.2f}% of the dataset, providing a highly balanced natural distribution.\n")
    f.write(f"3. Source '{largest_source}' contributes the largest number of emails ({source_counts.max()}), while '{smallest_source}' contributes the least ({source_counts.min()}).\n")
    f.write(f"4. The average word count across all emails is {avg_word_count:.2f} words.\n")
    f.write(f"5. A significant portion of emails contain URLs ({emails_with_urls} emails) and HTML ({emails_with_html} emails), which are common features analyzed in phishing detection.\n")
    
# Output final summary string for agent
summary = f"""EDA SUMMARY

Total Emails: {total_emails}
Legitimate: {total_legit}
Phishing: {total_phish}
Legitimate %: {pct_legit:.2f}%
Phishing %: {pct_phish:.2f}%

Largest Source: {largest_source}
Smallest Source: {smallest_source}

Average Subject Length: {avg_subj_len:.2f}
Average Email Length: {avg_body_len:.2f}
Average Word Count: {avg_word_count:.2f}

Emails Containing URLs: {emails_with_urls}
Emails Containing HTML: {emails_with_html}

Missing Values: {missing_values}
Duplicates: {exact_duplicates} (Exact) / {norm_duplicates} (Subject+Body)
Invalid Labels: {invalid_labels}
Outliers: 
{outliers_text}

Important Findings:
1. The dataset contains {total_emails} total emails.
2. Phishing emails represent {pct_phish:.2f}% of the dataset, providing a highly balanced natural distribution.
3. Source '{largest_source}' contributes the largest number of emails ({source_counts.max()}), while '{smallest_source}' contributes the least ({source_counts.min()}).
4. The average word count across all emails is {avg_word_count:.2f} words.
5. A significant portion of emails contain URLs ({emails_with_urls} emails) and HTML ({emails_with_html} emails), which are common features analyzed in phishing detection.
"""
print("EDA_SUMMARY_DELIMITER")
print(summary)
