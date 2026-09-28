import pandas as pd
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizerFast
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import sys

class EmailDataset(Dataset):
    def __init__(self, df, tokenizer):
        self.df = df
        self.tokenizer = tokenizer
        
    def __len__(self):
        return len(self.df)
        
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        subject = str(row['subject']) if pd.notna(row['subject']) else ""
        body = str(row['body']) if pd.notna(row['body']) else ""
        
        # Determine label (assuming string or int)
        label_val = row['label']
        if isinstance(label_val, str):
            label = 1 if label_val.lower() == 'phishing' else 0
        else:
            label = int(label_val)
            
        text = f"[SUBJECT]\n{subject}\n\n[BODY]\n{body}"
        
        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=256,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

def get_predictions(csv_path, model_dir='models/bert_phishing', batch_size=128):
    df = pd.read_csv(csv_path)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}", file=sys.stderr)
    model = BertForSequenceClassification.from_pretrained(model_dir).to(device)
    model.eval()
    tokenizer = BertTokenizerFast.from_pretrained(model_dir)
    
    dataset = EmailDataset(df, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=0)
    
    all_probs = []
    all_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].cpu().numpy()
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            probs = F.softmax(outputs.logits, dim=1).cpu().numpy()
            
            all_probs.extend(probs[:, 1])
            all_labels.extend(labels)
            
    return all_labels, all_probs

if __name__ == '__main__':
    val_labels, val_probs = get_predictions('data/processed/validation.csv')
    
    thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    
    print("VALIDATION METRICS:")
    print("Threshold | Acc | Prec | Rec | F1 | FPR | FNR | TP | TN | FP | FN")
    for t in thresholds:
        preds = [1 if p > t else 0 for p in val_probs]
        tn, fp, fn, tp = confusion_matrix(val_labels, preds).ravel()
        acc = accuracy_score(val_labels, preds)
        prec = precision_score(val_labels, preds, zero_division=0)
        rec = recall_score(val_labels, preds, zero_division=0)
        f1 = f1_score(val_labels, preds, zero_division=0)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        print(f"{t:.2f} | {acc:.4f} | {prec:.4f} | {rec:.4f} | {f1:.4f} | {fpr:.4f} | {fnr:.4f} | {tp} | {tn} | {fp} | {fn}")
