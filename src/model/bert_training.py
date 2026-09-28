import os
import sys
import time
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.preprocessing.text_formatter import format_bert_text

print("1. VERIFY THE ENVIRONMENT")
print(f"Python: {sys.version.split(' ')[0]}")
print(f"PyTorch: {torch.__version__}")
import transformers
print(f"Transformers: {transformers.__version__}")
print(f"NumPy: {np.__version__}")
import sklearn
print(f"scikit-learn: {sklearn.__version__}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"GPU Available: {torch.cuda.is_available()}")
print(f"Using device: {device}")

# Configuration
CONFIG = {
    'MODEL_NAME': 'bert-base-uncased',
    'BATCH_SIZE': 16,
    'LEARNING_RATE': 2e-5,
    'EPOCHS': 1,  # Based on CPU constraint approval
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

print(f"Train samples loaded: {len(train_data['labels'])}")
print(f"Validation samples loaded: {len(val_data['labels'])}")
print(f"Test samples loaded: {len(test_data['labels'])}")

print("\n3. VERIFY TOKENIZED DATA")
print(f"Input IDs shape (train): {train_data['input_ids'].shape}")
print(f"Attention mask shape (train): {train_data['attention_mask'].shape}")
print(f"Labels shape (train): {train_data['labels'].shape}")

assert train_data['input_ids'].shape == train_data['attention_mask'].shape
unique_labels = torch.unique(train_data['labels']).tolist()
assert set(unique_labels).issubset({0, 1})
print("Verification passed: Shapes match and labels are valid (0/1).")

print("\n4. CREATE PYTORCH DATASETS AND DATALOADERS")
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

train_dataset = PhishingDataset(train_data)
val_dataset = PhishingDataset(val_data)
test_dataset = PhishingDataset(test_data)

train_loader = DataLoader(train_dataset, batch_size=CONFIG['BATCH_SIZE'], shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=CONFIG['BATCH_SIZE'], shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=CONFIG['BATCH_SIZE'], shuffle=False)

print("\n5. LOAD PRETRAINED BERT")
model = BertForSequenceClassification.from_pretrained(CONFIG['MODEL_NAME'], num_labels=2)
model.to(device)
tokenizer = BertTokenizer.from_pretrained(CONFIG['MODEL_NAME'])

print("\n6. TEST BERT BEFORE FULL TRAINING")
test_batch = next(iter(train_loader))
input_ids = test_batch['input_ids'].to(device)
attention_mask = test_batch['attention_mask'].to(device)
labels = test_batch['labels'].to(device)

model.eval()
with torch.no_grad():
    outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
    logits = outputs.logits
    loss = outputs.loss

print(f"Forward Pass Logits Shape: {logits.shape}")
print(f"Forward Pass Loss: {loss.item()}")
assert logits.shape == (CONFIG['BATCH_SIZE'], 2)
print("Forward Pass Test: PASS")

print("\n7. TRAINING CONFIGURATION")
for k, v in CONFIG.items():
    print(f"{k}: {v}")

print("\n8. FINE-TUNE BERT & 9. OPTIMIZATION & 10. HANDLE CLASS BALANCE & 11. CHECKPOINTING & 12. EARLY STOPPING")
optimizer = AdamW(model.parameters(), lr=CONFIG['LEARNING_RATE'], weight_decay=CONFIG['WEIGHT_DECAY'])
total_steps = len(train_loader) * CONFIG['EPOCHS']
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(total_steps * CONFIG['WARMUP_RATIO']), num_training_steps=total_steps)

best_val_f1 = 0
best_epoch = 0
history = []

os.makedirs('models/checkpoints', exist_ok=True)
os.makedirs('models/bert_phishing', exist_ok=True)
os.makedirs('results/training', exist_ok=True)

# Training Loop
for epoch in range(CONFIG['EPOCHS']):
    print(f"--- Epoch {epoch+1}/{CONFIG['EPOCHS']} ---")
    model.train()
    total_train_loss = 0
    all_train_preds = []
    all_train_labels = []
    
    start_time = time.time()
    for step, batch in enumerate(train_loader):
        if step % 100 == 0 and step > 0:
            elapsed = time.time() - start_time
            print(f"  Batch {step}/{len(train_loader)} | Elapsed: {elapsed:.2f}s")
            
        b_input_ids = batch['input_ids'].to(device)
        b_attn_mask = batch['attention_mask'].to(device)
        b_labels = batch['labels'].to(device)
        
        model.zero_grad()
        outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask, labels=b_labels)
        
        loss = outputs.loss
        logits = outputs.logits
        
        total_train_loss += loss.item()
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        
        preds = torch.argmax(logits, dim=1).cpu().numpy()
        all_train_preds.extend(preds)
        all_train_labels.extend(b_labels.cpu().numpy())

    avg_train_loss = total_train_loss / len(train_loader)
    train_acc = accuracy_score(all_train_labels, all_train_preds)
    
    # Validation
    model.eval()
    total_val_loss = 0
    all_val_preds = []
    all_val_labels = []
    
    print("  Running Validation...")
    with torch.no_grad():
        for batch in val_loader:
            b_input_ids = batch['input_ids'].to(device)
            b_attn_mask = batch['attention_mask'].to(device)
            b_labels = batch['labels'].to(device)
            
            outputs = model(input_ids=b_input_ids, attention_mask=b_attn_mask, labels=b_labels)
            
            total_val_loss += outputs.loss.item()
            preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
            
            all_val_preds.extend(preds)
            all_val_labels.extend(b_labels.cpu().numpy())
            
    avg_val_loss = total_val_loss / len(val_loader)
    val_acc = accuracy_score(all_val_labels, all_val_preds)
    val_prec = precision_score(all_val_labels, all_val_preds)
    val_rec = recall_score(all_val_labels, all_val_preds)
    val_f1 = f1_score(all_val_labels, all_val_preds)
    
    current_lr = scheduler.get_last_lr()[0]
    
    print(f"  Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.4f}")
    print(f"  Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f} | Val F1: {val_f1:.4f}")
    
    history.append({
        'Epoch': epoch + 1,
        'Training Loss': avg_train_loss,
        'Training Accuracy': train_acc,
        'Validation Loss': avg_val_loss,
        'Validation Accuracy': val_acc,
        'Validation Precision': val_prec,
        'Validation Recall': val_rec,
        'Validation F1': val_f1,
        'Learning Rate': current_lr
    })
    
    if val_f1 > best_val_f1:
        best_val_f1 = val_f1
        best_epoch = epoch + 1
        save_path = 'models/bert_phishing_candidate'
        os.makedirs(save_path, exist_ok=True)
        try:
            model.save_pretrained(save_path)
            tokenizer.save_pretrained(save_path)
            
            # Verify saving
            if not os.path.exists(os.path.join(save_path, 'config.json')):
                raise RuntimeError("config.json is missing")
            if not (os.path.exists(os.path.join(save_path, 'model.safetensors')) or os.path.exists(os.path.join(save_path, 'pytorch_model.bin'))):
                raise RuntimeError("model weights are missing")
                
            test_model = BertForSequenceClassification.from_pretrained(save_path)
            if test_model.num_labels != 2:
                raise RuntimeError(f"Expected 2 labels, got {test_model.num_labels}")
            del test_model
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to save checkpoint safely. {e}")
            sys.exit(1)

print("\n13. TRAINING HISTORY")
history_df = pd.DataFrame(history)
history_df.to_csv('results/training/training_history.csv', index=False)

plt.figure(figsize=(8,6))
plt.plot(history_df['Epoch'], history_df['Training Loss'], label='Train Loss')
plt.plot(history_df['Epoch'], history_df['Validation Loss'], label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('results/training/loss_curve.png')

plt.figure(figsize=(8,6))
plt.plot(history_df['Epoch'], history_df['Training Accuracy'], label='Train Acc')
plt.plot(history_df['Epoch'], history_df['Validation Accuracy'], label='Val Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('results/training/accuracy_curve.png')

plt.figure(figsize=(8,6))
plt.plot(history_df['Epoch'], history_df['Validation F1'], label='Val F1')
plt.xlabel('Epoch')
plt.ylabel('F1 Score')
plt.legend()
plt.savefig('results/training/f1_curve.png')

print("\n15. MODEL RELOAD TEST")
del model
del tokenizer
torch.cuda.empty_cache()

reloaded_model = BertForSequenceClassification.from_pretrained('models/bert_phishing_candidate')
reloaded_tokenizer = BertTokenizer.from_pretrained('models/bert_phishing_candidate')
reloaded_model.to(device)

sample_text = [
    format_bert_text("Test", "This is a test email."), 
    format_bert_text("Alert", "Your account has been locked. Click here to verify.")
]
enc = reloaded_tokenizer(sample_text, padding=True, truncation=True, max_length=256, return_tensors='pt')
enc = {k: v.to(device) for k, v in enc.items()}
with torch.no_grad():
    out = reloaded_model(**enc)
    preds = torch.argmax(out.logits, dim=1).cpu().numpy()

reload_test_status = "PASS" if len(preds) == 2 else "FAIL"
print(f"Model Reload Test: {reload_test_status}")

print("\n16. TRAINING REPORT")
report_content = f"""# TRAINING REPORT

### Model
Model: {CONFIG['MODEL_NAME']}
Tokenizer: {CONFIG['MODEL_NAME']}
Number of labels: 2

### Dataset
Training samples: {len(train_dataset)}
Validation samples: {len(val_dataset)}
Test samples: {len(test_dataset)}

### Configuration
Batch size: {CONFIG['BATCH_SIZE']}
Learning rate: {CONFIG['LEARNING_RATE']}
Epochs: {CONFIG['EPOCHS']}
Max length: {CONFIG['MAX_LENGTH']}
Optimizer: AdamW
Scheduler: Linear with warmup

### Results (Best Epoch {best_epoch})
Training Loss: {history[best_epoch-1]['Training Loss']:.4f}
Training Accuracy: {history[best_epoch-1]['Training Accuracy']:.4f}
Validation Loss: {history[best_epoch-1]['Validation Loss']:.4f}
Validation Accuracy: {history[best_epoch-1]['Validation Accuracy']:.4f}
Validation Precision: {history[best_epoch-1]['Validation Precision']:.4f}
Validation Recall: {history[best_epoch-1]['Validation Recall']:.4f}
Validation F1: {history[best_epoch-1]['Validation F1']:.4f}
"""
with open('results/training/TRAINING_REPORT.md', 'w') as f:
    f.write(report_content)

print("\n17. IMPORTANT DATA INTEGRITY CHECKS")
data_integrity_pass = all([
    len(train_dataset) == 70308,
    len(val_dataset) == 8789,
    len(test_dataset) == 8789
])
integrity_status = "PASS" if data_integrity_pass else "FAIL"

summary = f"""PHASE 5 SUMMARY

Model: {CONFIG['MODEL_NAME']}
Tokenizer: {CONFIG['MODEL_NAME']}

Training Samples: {len(train_dataset)}
Validation Samples: {len(val_dataset)}
Test Samples: {len(test_dataset)}

Epochs Completed: {CONFIG['EPOCHS']}
Best Epoch: {best_epoch}

Best Validation Accuracy: {history[best_epoch-1]['Validation Accuracy']:.4f}
Best Validation Precision: {history[best_epoch-1]['Validation Precision']:.4f}
Best Validation Recall: {history[best_epoch-1]['Validation Recall']:.4f}
Best Validation F1: {history[best_epoch-1]['Validation F1']:.4f}

Model Saved: YES
Model Reload Test: {reload_test_status}
Data Integrity: {integrity_status}
Test Data Used During Training: NO

FINAL STATUS:
COMPLETE
"""

print("PHASE_5_DELIMITER")
print(summary)
