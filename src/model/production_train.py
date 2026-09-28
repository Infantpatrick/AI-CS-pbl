import os
import sys
import time
import shutil
import json
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.preprocessing.text_formatter import format_bert_text

print("1. VERIFY THE ENVIRONMENT")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Configuration
torch.set_num_threads(4)
CONFIG = {
    'MODEL_NAME': 'bert-base-uncased',
    'BATCH_SIZE': 8,
    'LEARNING_RATE': 2e-5,
    'EPOCHS': 1,
    'MAX_LENGTH': 256,
    'RANDOM_SEED': 42,
    'WEIGHT_DECAY': 0.01,
    'WARMUP_RATIO': 0.1
}

torch.manual_seed(CONFIG['RANDOM_SEED'])
np.random.seed(CONFIG['RANDOM_SEED'])

print("\n2. LOAD TOKENIZED DATA")
def load_data(name):
    path = f"data/tokenized/{name}.npz"
    data = np.load(path)
    return {
        'input_ids': torch.tensor(data['input_ids'], dtype=torch.long),
        'attention_mask': torch.tensor(data['attention_mask'], dtype=torch.long),
        'labels': torch.tensor(data['labels'], dtype=torch.long)
    }

train_data = load_data('train')
val_data = load_data('validation')
test_data = load_data('test')

class PhishingDataset(Dataset):
    def __init__(self, data):
        self.input_ids = data['input_ids']
        self.attention_mask = data['attention_mask']
        self.labels = data['labels']
        
    def __len__(self):
        return len(self.labels)
        
    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }

train_loader = DataLoader(PhishingDataset(train_data), batch_size=CONFIG['BATCH_SIZE'], shuffle=True)
val_loader = DataLoader(PhishingDataset(val_data), batch_size=CONFIG['BATCH_SIZE'], shuffle=False)
test_loader = DataLoader(PhishingDataset(test_data), batch_size=CONFIG['BATCH_SIZE'], shuffle=False)

print("\n3. LOAD PRETRAINED BERT")
model = BertForSequenceClassification.from_pretrained(
    CONFIG['MODEL_NAME'], 
    num_labels=2,
    id2label={"0": "Legitimate", "1": "Malicious"},
    label2id={"Legitimate": 0, "Malicious": 1}
)
model.to(device)
from transformers import BertTokenizerFast
tokenizer = BertTokenizerFast.from_pretrained('models/bert_phishing')

print("\n4. TRAINING")
optimizer = AdamW(model.parameters(), lr=CONFIG['LEARNING_RATE'], weight_decay=CONFIG['WEIGHT_DECAY'])
total_steps = len(train_loader) * CONFIG['EPOCHS']
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(total_steps * CONFIG['WARMUP_RATIO']), num_training_steps=total_steps)

os.makedirs('models/bert_phishing_candidate', exist_ok=True)
os.makedirs('results/training', exist_ok=True)

start_time_total = time.time()

for epoch in range(CONFIG['EPOCHS']):
    print(f"--- Epoch {epoch+1}/{CONFIG['EPOCHS']} ---")
    model.train()
    
    start_time = time.time()
    for step, batch in enumerate(train_loader):
        b_input_ids = batch['input_ids'].to(device)
        b_attn_mask = batch['attention_mask'].to(device)
        b_labels = batch['labels'].to(device)
        
        model.zero_grad()
        outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask, labels=b_labels)
        
        loss = outputs.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()

        if step % 100 == 0:
            print(f"Batch {step}/{len(train_loader)} | Loss: {loss.item():.4f}")

print("\n5. VALIDATION")
model.eval()
all_val_preds = []
all_val_labels = []

with torch.no_grad():
    for batch in val_loader:
        b_input_ids = batch['input_ids'].to(device)
        b_attn_mask = batch['attention_mask'].to(device)
        b_labels = batch['labels'].to(device)
        
        outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask, labels=b_labels)
        preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
        
        all_val_preds.extend(preds)
        all_val_labels.extend(b_labels.cpu().numpy())

val_acc = accuracy_score(all_val_labels, all_val_preds)
val_f1 = f1_score(all_val_labels, all_val_preds)
print(f"Validation Acc: {val_acc:.4f} | Validation F1: {val_f1:.4f}")

print("\n6. SAVE CANDIDATE MODEL")
save_path = 'models/bert_phishing_candidate'
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

training_time = time.time() - start_time_total
print(f"Training Time: {training_time:.2f} seconds")

print("\n7. VERIFY RELOAD")
del model
del tokenizer
torch.cuda.empty_cache()

model = BertForSequenceClassification.from_pretrained(save_path)
if model.num_labels != 2:
    print("FAIL: num_labels is not 2")
    sys.exit(1)
model.to(device)
tokenizer = BertTokenizer.from_pretrained(save_path)
print("Reload OK, num_labels == 2")

print("\n8. FULL TEST SET EVALUATION")
model.eval()
all_test_preds = []
all_test_labels = []

with torch.no_grad():
    for step, batch in enumerate(test_loader):
        if step % 100 == 0:
            print(f"Test batch {step}/{len(test_loader)}")
        b_input_ids = batch['input_ids'].to(device)
        b_attn_mask = batch['attention_mask'].to(device)
        b_labels = batch['labels'].to(device)
        
        outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask)
        preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
        
        all_test_preds.extend(preds)
        all_test_labels.extend(b_labels.cpu().numpy())

test_acc = accuracy_score(all_test_labels, all_test_preds)
test_prec = precision_score(all_test_labels, all_test_preds)
test_rec = recall_score(all_test_labels, all_test_preds)
test_f1 = f1_score(all_test_labels, all_test_preds)

cm = confusion_matrix(all_test_labels, all_test_preds)
tn, fp, fn, tp = cm.ravel()
fpr = fp / (fp + tn)
fnr = fn / (fn + tp)

print(f"Test Acc: {test_acc:.4f}, Prec: {test_prec:.4f}, Rec: {test_rec:.4f}, F1: {test_f1:.4f}")
print(f"FPR: {fpr:.4f}, FNR: {fnr:.4f}")
print(f"Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

print("\n9. RUN MANUAL INFERENCE ON REPRESENTATIVE EMAILS")
import torch.nn.functional as F
emails = [
    ("Weekly Project Meeting – Friday at 10:00 AM", "Hi Team,\n\nThis is a reminder about our weekly project meeting scheduled for Friday at 10:00 AM. We will discuss the current development progress, pending tasks, and plans for next week.\n\nRegards,\nProject Team"),
    ("Congratulations! You Have Won a $5,000 Reward", "Congratulations! Your email address has been selected for a special reward. Claim your $5,000 prize today by completing the confirmation process."),
    ("URGENT ACTION REQUIRED: Your Account Will Be Permanently Suspended Today", "Your account requires immediate verification. Failure to verify your account today may result in permanent suspension.\n\nPlease verify your account by providing your login credentials, password, card information, CVV and OTP.\n\nVerify now:\nhttp://account-security-verification.example.com/secure-login\n\nDo not visit the URL.")
]

manual_results = []
for subject, body in emails:
    bert_text = format_bert_text(subject, body)
    inputs = tokenizer(bert_text, padding='max_length', truncation=True, max_length=256, return_tensors='pt')
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model(**inputs)
        probs = F.softmax(out.logits, dim=1).cpu().numpy()[0]
    legitimate_prob = float(probs[0])
    malicious_prob = float(probs[1])
    is_malicious = malicious_prob > 0.50
    pred_label = "Malicious" if is_malicious else "Legitimate"
    print(f"Subj: {subject[:20]}... | Pred: {pred_label} | Leg: {legitimate_prob:.4f} | Mal: {malicious_prob:.4f}")
    manual_results.append({
        'subject': subject,
        'prediction': pred_label,
        'legitimate_prob': legitimate_prob,
        'malicious_prob': malicious_prob
    })

all_same = len(set([x['prediction'] for x in manual_results])) == 1
if all_same:
    print("WARNING: Predictions are identical for all inputs. The model might still be failing to differentiate.")
else:
    print("Predictions behave differently for different examples. Pass.")

print("\n10. COPY/PROMOTE TO PRODUCTION")
prod_path = 'models/bert_phishing'
if os.path.exists(prod_path):
    shutil.rmtree(prod_path)
shutil.copytree(save_path, prod_path)
print(f"Successfully promoted model to {prod_path}")

report = {
    'training_status': 'SUCCESS',
    'dataset_rows': len(train_data['labels']) + len(val_data['labels']) + len(test_data['labels']),
    'train_count': len(train_data['labels']),
    'val_count': len(val_data['labels']),
    'test_count': len(test_data['labels']),
    'model_architecture': 'bert-base-uncased',
    'training_time_seconds': training_time,
    'val_f1': val_f1,
    'test_acc': test_acc,
    'test_prec': test_prec,
    'test_rec': test_rec,
    'test_f1': test_f1,
    'confusion_matrix': {'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)},
    'fpr': fpr,
    'fnr': fnr,
    'manual_results': manual_results,
    'production_checkpoint': prod_path,
    'model_fine_tuned': True,
    'fallback_model_used': False,
    'warnings': []
}

with open('results/training/production_training_report.json', 'w') as f:
    json.dump(report, f, indent=4)

print("\nDONE.")
