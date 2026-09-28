import os
import pandas as pd
import chardet

raw_dir = 'data/raw'
inventory_data = []
label_data = []

# Using predefined mappings for the assignment, assuming we just inspect existing datasets
for root, dirs, files in os.walk(raw_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            source = os.path.basename(root)
            dataset_name = file.replace('.csv', '')
            
            # Detect encoding roughly
            with open(file_path, 'rb') as f:
                raw_bytes = f.read(100000)
                encoding_result = chardet.detect(raw_bytes)
                encoding = encoding_result['encoding'] or 'utf-8'
                
            try:
                df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
            except Exception as e:
                try:
                    encoding = 'latin-1'
                    df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
                except Exception as e2:
                    print(f"Error reading {file_path}: {e2}")
                    continue
                    
            file_size = os.path.getsize(file_path)
            num_records = len(df)
            num_columns = len(df.columns)
            columns = df.columns.tolist()
            
            inventory_data.append({
                'Dataset Name': dataset_name,
                'Source': source,
                'File Name': file,
                'File Format': 'csv',
                'Number of Records': num_records,
                'Number of Columns': num_columns,
                'Column Names': ', '.join(columns),
                'Encoding': encoding,
                'File Size': file_size,
                'License/Usage Information': 'Unknown'
            })
            
            # Find label column
            label_col = None
            for col in columns:
                if col.lower() in ['label', 'email type', 'class', 'target']:
                    label_col = col
                    break
            
            if label_col:
                # Count unique labels
                label_counts = df[label_col].value_counts(dropna=False)
                for orig_label, count in label_counts.items():
                    orig_label_str = str(orig_label)
                    orig_label_lower = orig_label_str.lower().strip()
                    
                    # Propose standard label
                    standard = 'Review'
                    if orig_label_lower in ['0', 'ham', 'legitimate', 'safe', 'Phishing Email']:
                        if orig_label_lower == 'phishing email': # Note: wait, Phishing Email dataset uses "Phishing Email" and "Safe Email"? Let's just say Review for now.
                            pass
                        elif orig_label_lower in ['0', 'ham', 'legitimate', 'safe']:
                            standard = '0'
                    if orig_label_lower in ['1', 'spam', 'phishing', 'fraud']:
                        standard = '1'
                    if orig_label_lower == 'phishing email':
                        standard = '1'
                    if orig_label_lower == 'safe email':
                        standard = '0'
                        
                    label_data.append({
                        'Dataset': dataset_name,
                        'Original Label': orig_label_str,
                        'Count': count,
                        'Meaning': 'To be reviewed' if standard == 'Review' else ('Legitimate' if standard == '0' else 'Phishing/Spam/Fraud'),
                        'Proposed Standard Label': standard
                    })

# Save inventory
inv_df = pd.DataFrame(inventory_data)
inv_df.to_csv('data/dataset_inventory.csv', index=False)

# Save label mapping
lbl_df = pd.DataFrame(label_data)
lbl_df.to_csv('data/label_mapping.csv', index=False)

print("Inventory and label mapping complete.")
print(lbl_df)
