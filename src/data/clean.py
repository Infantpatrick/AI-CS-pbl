import os
import pandas as pd
import re
import html
import uuid

raw_dir = 'data/raw'
inter_dir = 'data/intermediate'

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Decode HTML entities
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_datasets():
    lbl_df = pd.read_csv('data/label_mapping.csv')
    label_map = dict(zip(lbl_df['Dataset'] + "_" + lbl_df['Original Label'].astype(str).str.lower(), lbl_df['Proposed Standard Label']))
    
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                source = os.path.basename(root)
                dataset_name = file.replace('.csv', '')
                print(f"Processing {dataset_name}...")
                
                try:
                    df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
                except Exception:
                    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
                
                # Standardize columns
                col_map = {}
                for col in df.columns:
                    col_lower = col.lower().strip()
                    if col_lower in ['subject']:
                        col_map[col] = 'subject'
                    elif col_lower in ['body', 'email text', 'message']:
                        col_map[col] = 'body'
                    elif col_lower in ['label', 'email type', 'class', 'target']:
                        col_map[col] = 'original_label'
                        
                df = df.rename(columns=col_map)
                
                # Add missing columns
                if 'subject' not in df.columns:
                    df['subject'] = ""
                if 'body' not in df.columns:
                    df['body'] = ""
                if 'original_label' not in df.columns:
                    df['original_label'] = "Unknown"
                    
                # Clean text
                df['subject'] = df['subject'].apply(clean_text)
                df['body'] = df['body'].apply(clean_text)
                
                # Create bert_text
                df['bert_text'] = "[SUBJECT]\n" + df['subject'] + "\n\n[BODY]\n" + df['body']
                
                # Assign standard labels
                df['label'] = df['original_label'].astype(str).str.lower().apply(
                    lambda x: label_map.get(f"{dataset_name}_{x}", 'Review')
                )
                
                df['source'] = source
                df['email_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
                
                # Select only required columns
                df = df[['email_id', 'subject', 'body', 'bert_text', 'label', 'source', 'original_label']]
                
                # Save to intermediate
                out_path = os.path.join(inter_dir, f"{dataset_name}_cleaned.csv")
                df.to_csv(out_path, index=False)

if __name__ == "__main__":
    process_datasets()
    print("Formatting and cleaning complete.")
