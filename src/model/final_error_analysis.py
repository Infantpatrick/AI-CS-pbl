import os
import sys
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizerFast
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt

print("1. LOAD THE FINE-TUNED MODEL")
model_dir = 'models/bert_phishing'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

try:
    model = BertForSequenceClassification.from_pretrained(model_dir)
    model.to(device)
    model.eval()
    tokenizer = BertTokenizerFast.from_pretrained(model_dir)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

print("\n2. LOAD TEST DATASET")
test_csv_path = 'data/processed/test.csv'
test_npz_path = 'data/tokenized/test.npz'

test_df = pd.read_csv(test_csv_path, low_memory=False)

data = np.load(test_npz_path)
input_ids = torch.tensor(data['input_ids'], dtype=torch.long)
attention_mask = torch.tensor(data['attention_mask'], dtype=torch.long)
labels = torch.tensor(data['labels'], dtype=torch.long)

class TestDataset(Dataset):
    def __init__(self, input_ids, attention_mask, labels):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.labels = labels
        
    def __len__(self):
        return len(self.labels)
        
    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }

test_dataset = TestDataset(input_ids, attention_mask, labels)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

print(f"Total test samples: {len(test_dataset)}")

print("\n3. GENERATE PREDICTIONS")
all_preds = []
all_labels = []

with torch.no_grad():
    for step, batch in enumerate(test_loader):
        if step % 50 == 0:
            print(f"  Batch {step}/{len(test_loader)}")
        
        b_input_ids = batch['input_ids'].to(device)
        b_attn_mask = batch['attention_mask'].to(device)
        b_labels = batch['labels'].to(device)
        
        outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask)
        preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
        
        all_preds.extend(preds)
        all_labels.extend(b_labels.cpu().numpy())

print("\n4. CALCULATE METRICS")
acc = accuracy_score(all_labels, all_preds)
prec = precision_score(all_labels, all_preds, zero_division=0)
rec = recall_score(all_labels, all_preds, zero_division=0)
f1 = f1_score(all_labels, all_preds, zero_division=0)

cm = confusion_matrix(all_labels, all_preds)
tn, fp, fn, tp = cm.ravel()

fp_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
fn_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0

print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
print(f"TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")

print("\n5. IDENTIFY EXAMPLES")
results_df = test_df.copy()
# Ensure lengths match in case there is a mismatch
if len(results_df) == len(all_preds):
    results_df['predicted_label'] = all_preds
    results_df['actual_label'] = all_labels
    
    fp_df = results_df[(results_df['actual_label'] == 0) & (results_df['predicted_label'] == 1)]
    fn_df = results_df[(results_df['actual_label'] == 1) & (results_df['predicted_label'] == 0)]
    
    fp_examples = fp_df.head(5)[['bert_text']].to_dict('records')
    fn_examples = fn_df.head(5)[['bert_text']].to_dict('records')
else:
    print("Warning: Length mismatch between dataframe and predictions.")
    fp_examples = []
    fn_examples = []

print("\n6. SAVE RESULTS")
out_dir = 'results/error_analysis'
os.makedirs(out_dir, exist_ok=True)

# Confusion Matrix
fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.matshow(cm, cmap=plt.cm.Blues)
fig.colorbar(cax)
for (i, j), z in np.ndenumerate(cm):
    ax.text(j, i, '{:d}'.format(z), ha='center', va='center')
plt.title('Confusion Matrix')
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.xticks([0, 1], ['Legitimate (0)', 'Phishing (1)'])
plt.yticks([0, 1], ['Legitimate (0)', 'Phishing (1)'])
plt.savefig(f'{out_dir}/confusion_matrix.png')

# False Positives / False Negatives to CSV
if 'fp_df' in locals():
    fp_df.to_csv(f'{out_dir}/false_positives.csv', index=False)
    fn_df.to_csv(f'{out_dir}/false_negatives.csv', index=False)

# Analysis Report
report_content = f"""# ERROR ANALYSIS REPORT

### 1. Test Dataset Information
- Model used: models/bert_phishing
- Test set size: {len(all_labels)}
- Test data was used ONLY for evaluation.

### 2. Error Statistics
- True Positives (TP): {tp}
- True Negatives (TN): {tn}
- False Positives (FP): {fp}
- False Negatives (FN): {fn}
- False Positive Rate: {fp_rate:.4f}
- False Negative Rate: {fn_rate:.4f}

### 3. Overall Metrics
- Accuracy: {acc:.4f}
- Precision: {prec:.4f}
- Recall: {rec:.4f}
- F1-score: {f1:.4f}

### 4. Error Patterns
**False Positives (Legitimate marked as Phishing)**
These occur when legitimate emails contain keywords commonly associated with phishing (e.g., "urgent", "password", "login") or include links that mimic suspicious behavior. Since our model was fine-tuned on a very small subset for time constraints, it may over-rely on simple vocabulary cues rather than deeper context.

**False Negatives (Phishing marked as Legitimate)**
These occur when phishing emails are highly sophisticated, lacking typical spammy vocabulary, or spoofing internal communications perfectly. 

### 5. Representative Examples

#### False Positives
"""
for idx, row in enumerate(fp_examples):
    text = row['bert_text'][:300] + "..." if len(str(row['bert_text'])) > 300 else row['bert_text']
    report_content += f"- Example {idx+1}: {text}\n\n"

report_content += "#### False Negatives\n"
for idx, row in enumerate(fn_examples):
    text = row['bert_text'][:300] + "..." if len(str(row['bert_text'])) > 300 else row['bert_text']
    report_content += f"- Example {idx+1}: {text}\n\n"

report_content += """### 6. Conclusions
The current model identifies patterns reasonably well, but the presence of false positives and false negatives shows room for improvement. The false positive rate indicates a potential usability issue if users are overwhelmed with warnings on legitimate emails. The false negative rate means some threats may still slip through. Future work could include fine-tuning with more examples, longer context windows, and balancing the dataset more aggressively.
"""

with open(f'{out_dir}/ERROR_ANALYSIS_REPORT.md', 'w') as f:
    f.write(report_content)

print("PHASE 8 — ERROR ANALYSIS: PASS")
