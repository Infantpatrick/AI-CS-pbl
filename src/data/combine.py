import os
import pandas as pd
import hashlib

inter_dir = 'data/intermediate'
proc_dir = 'data/processed'
reports_dir = 'data'

def generate_reports():
    dfs = []
    for file in os.listdir(inter_dir):
        if file.endswith('.csv'):
            dfs.append(pd.read_csv(os.path.join(inter_dir, file), low_memory=False))
            
    if not dfs:
        print("No intermediate files found.")
        return
        
    df = pd.concat(dfs, ignore_index=True)
    
    total_raw_emails = len(df)
    
    # Missing values
    missing_subj = df['subject'].isna().sum() + (df['subject'] == '').sum()
    missing_body = df['body'].isna().sum() + (df['body'] == '').sum()
    missing_label = df['label'].isna().sum() + (df['label'] == 'Review').sum()
    
    # Drop rows without label
    df = df[df['label'].isin(['0', '1', 0, 1])].copy()
    
    # Ensure string types
    df['subject'] = df['subject'].fillna('').astype(str)
    df['body'] = df['body'].fillna('').astype(str)
    
    # Normalization for deduplication
    df['norm_text'] = (df['subject'] + df['body']).str.lower().str.replace(r'\s+', '', regex=True)
    
    # Exact Duplicates (on bert_text)
    total_before_dup = len(df)
    exact_dups = df.duplicated(subset=['bert_text']).sum()
    
    df_no_exact = df.drop_duplicates(subset=['bert_text']).copy()
    
    # Normalized Duplicates
    norm_dups = df_no_exact.duplicated(subset=['norm_text']).sum()
    
    df_final = df_no_exact.drop_duplicates(subset=['norm_text']).copy()
    records_remaining = len(df_final)
    
    dup_report = pd.DataFrame([{
        'Total records before duplicates': total_before_dup,
        'Exact duplicates': exact_dups,
        'Normalized duplicates': norm_dups,
        'Records remaining': records_remaining
    }])
    dup_report.to_csv(os.path.join(reports_dir, 'duplicate_report.csv'), index=False)
    
    # Data quality check
    empty_emails = len(df_final[(df_final['subject'] == '') & (df_final['body'] == '')])
    invalid_labels = df_final[~df_final['label'].astype(str).isin(['0', '1'])].shape[0]
    
    dq_report = pd.DataFrame([{
        'Check': 'Missing Subject', 'Count': missing_subj
    }, {
        'Check': 'Missing Body', 'Count': missing_body
    }, {
        'Check': 'Missing/Review Labels Removed', 'Count': missing_label
    }, {
        'Check': 'Empty Emails Remaining', 'Count': empty_emails
    }, {
        'Check': 'Invalid Labels Remaining', 'Count': invalid_labels
    }])
    dq_report.to_csv(os.path.join(reports_dir, 'data_quality_report.csv'), index=False)
    
    # Drop temp columns
    df_final = df_final.drop(columns=['norm_text'])
    
    # Final Output
    df_final.to_csv(os.path.join(proc_dir, 'email_phishing_dataset.csv'), index=False)
    
    # Stats
    legitimate_count = len(df_final[df_final['label'].astype(str) == '0'])
    phishing_count = len(df_final[df_final['label'].astype(str) == '1'])
    
    # Markdown report
    with open('DATA_COLLECTION_REPORT.md', 'w') as f:
        f.write("# DATA COLLECTION SUMMARY\n\n")
        f.write(f"Total raw emails: {total_raw_emails}\n")
        f.write(f"Total cleaned emails: {records_remaining}\n")
        f.write(f"Legitimate: {legitimate_count}\n")
        f.write(f"Phishing: {phishing_count}\n")
        f.write(f"Duplicates removed: {exact_dups + norm_dups}\n")
        f.write(f"Missing/invalid records removed: {missing_label}\n")
        f.write("\n## Sources Distribution\n")
        sources = df_final['source'].value_counts()
        for src, count in sources.items():
            f.write(f"- {src}: {count}\n")
        f.write(f"\nFinal dataset path: {os.path.join(proc_dir, 'email_phishing_dataset.csv')}\n")

if __name__ == "__main__":
    generate_reports()
    print("Consolidation and reporting complete.")
