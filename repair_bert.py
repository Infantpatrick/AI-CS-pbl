import os
import sys
import shutil
import time
import json
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments

# Configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    acc = accuracy_score(labels, preds)
    precision = precision_score(labels, preds)
    recall = recall_score(labels, preds)
    f1 = f1_score(labels, preds)
    return {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }

class PhishingDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def main():
    print("==================================================")
    print("PHASE 2 — VERIFY DATA LOADING")
    print("==================================================")
    df = pd.read_csv('data/processed/email_phishing_dataset.csv')
    print(f"Total: {len(df)}")
    
    df['subject'] = df['subject'].fillna("")
    df['body'] = df['body'].fillna("")
    
    texts = []
    labels = []
    for _, row in df.iterrows():
        text = f"[SUBJECT]\n{row['subject']}\n\n[BODY]\n{row['body']}"
        texts.append(text)
        labels.append(int(row['label']))
        
    train_texts, temp_texts, train_labels, temp_labels = train_test_split(texts, labels, test_size=(17578/87886), random_state=42)
    val_texts, test_texts, val_labels, test_labels = train_test_split(temp_texts, temp_labels, test_size=0.5, random_state=42)
    
    print(f"Train: {len(train_texts)}")
    print(f"Validation: {len(val_texts)}")
    print(f"Test: {len(test_texts)}")

    print(f"Train labels: 0={train_labels.count(0)}, 1={train_labels.count(1)}")
    print(f"Val labels: 0={val_labels.count(0)}, 1={val_labels.count(1)}")
    print(f"Test labels: 0={test_labels.count(0)}, 1={test_labels.count(1)}")

    print("==================================================")
    print("PHASE 3 — TRAINING CONFIGURATION")
    print("==================================================")
    
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    
    print("Tokenizing...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=256)
    
    train_dataset = PhishingDataset(train_encodings, train_labels)
    val_dataset = PhishingDataset(val_encodings, val_labels)
    test_dataset = PhishingDataset(test_encodings, test_labels)
    
    id2label = {0: "LEGITIMATE", 1: "MALICIOUS"}
    label2id = {"LEGITIMATE": 0, "MALICIOUS": 1}
    
    model = BertForSequenceClassification.from_pretrained(
        'bert-base-uncased', 
        num_labels=2,
        id2label=id2label,
        label2id=label2id
    )
    
    out_dir = 'models/bert_phishing_candidate'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    training_args = TrainingArguments(
        output_dir=out_dir,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_steps=439,
        lr_scheduler_type="linear",
        eval_strategy="steps",
        eval_steps=500,
        logging_steps=100,
        save_strategy="steps",
        save_steps=500,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False,
        seed=42,
        fp16=torch.cuda.is_available(),
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    print("==================================================")
    print("PHASE 4 — TRAINING MONITORING")
    print("==================================================")
    print("Starting training...")
    start_time = time.time()
    trainer.train()
    train_time = time.time() - start_time
    print(f"Training completed in {train_time:.2f} seconds.")
    
    print("==================================================")
    print("PHASE 5 — CHECKPOINT SAFETY")
    print("==================================================")
    print("Saving candidate model...")
    trainer.save_model(out_dir)
    tokenizer.save_pretrained(out_dir)
    
    required_files = ['config.json', 'model.safetensors']
    for f in required_files:
        path = os.path.join(out_dir, f)
        print(f"File {f} exists: {os.path.exists(path)}")
        
    reloaded_model = BertForSequenceClassification.from_pretrained(out_dir)
    print(f"Reloaded num_labels: {reloaded_model.config.num_labels}")
    print(f"id2label: {reloaded_model.config.id2label}")
    print(f"label2id: {reloaded_model.config.label2id}")
    
    print("==================================================")
    print("PHASE 6 — SANITY TEST AFTER TRAINING")
    print("==================================================")
    test_emails = [
        # LEGITIMATE 1
        "[SUBJECT]\nWeekly Project Meeting – Friday at 10:00 AM\n\n[BODY]\nHi Team,\n\nThis is a reminder about our weekly project meeting scheduled for Friday at 10:00 AM. We will discuss current development progress and pending tasks.\n\nRegards,\nProject Team",
        # LEGITIMATE 2
        "[SUBJECT]\nYour Project Documentation Is Ready\n\n[BODY]\nHi Team,\n\nThe project documentation has been updated and is now available.\n\nYou can access the documentation here:\nhttps://docs.example.com/project/resources\n\nRegards,\nProject Team",
        # MALICIOUS 1
        "[SUBJECT]\nCongratulations! You Have Won a $5,000 Reward\n\n[BODY]\nCongratulations! Your email address has been selected for a special reward. Claim your prize today by completing the confirmation process.",
        # MALICIOUS 2
        "[SUBJECT]\nURGENT ACTION REQUIRED: Your Account Will Be Suspended\n\n[BODY]\nYour account requires immediate verification.\n\nPlease provide your password, card information, CVV and OTP.\n\nVerify here:\nhttp://account-security-verification.example.com/secure-login"
    ]
    
    reloaded_model.eval()
    if torch.cuda.is_available():
        reloaded_model.to('cuda')
        
    for i, email_text in enumerate(test_emails):
        inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding=True, max_length=256)
        if torch.cuda.is_available():
            inputs = {k: v.to('cuda') for k, v in inputs.items()}
            
        with torch.no_grad():
            outputs = reloaded_model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            probs_np = probs.cpu().numpy()[0]
            pred_class = int(np.argmax(probs_np))
            
            print(f"Test {i+1}:")
            print(f"  Legitimate probability: {probs_np[0]:.4f}")
            print(f"  Malicious probability: {probs_np[1]:.4f}")
            print(f"  Prediction: {id2label[pred_class]}")
            print(f"  Confidence: {np.max(probs_np):.4f}")
            
    print("==================================================")
    print("PHASE 7 — FULL TEST SET EVALUATION")
    print("==================================================")
    reloaded_trainer = Trainer(
        model=reloaded_model,
        args=TrainingArguments(output_dir='tmp_eval', per_device_eval_batch_size=16),
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )
    
    test_results = reloaded_trainer.predict(test_dataset)
    test_metrics = test_results.metrics
    print("Test Metrics:", test_metrics)
    
    preds = test_results.predictions.argmax(-1)
    cm = confusion_matrix(test_labels, preds)
    print("Confusion Matrix:")
    print(f"TN: {cm[0,0]}")
    print(f"FP: {cm[0,1]}")
    print(f"FN: {cm[1,0]}")
    print(f"TP: {cm[1,1]}")
    
    print("==================================================")
    print("PHASE 8 — PROBABILITY DISTRIBUTION")
    print("==================================================")
    probs_all = torch.nn.functional.softmax(torch.tensor(test_results.predictions), dim=-1).numpy()
    malicious_probs = probs_all[:, 1]
    
    test_labels_np = np.array(test_labels)
    legit_probs = malicious_probs[test_labels_np == 0]
    mal_probs = malicious_probs[test_labels_np == 1]
    
    print("LEGITIMATE TEST EMAILS (Malicious Probability):")
    print(f"  min: {np.min(legit_probs):.4f}")
    print(f"  max: {np.max(legit_probs):.4f}")
    print(f"  mean: {np.mean(legit_probs):.4f}")
    print(f"  median: {np.median(legit_probs):.4f}")
    
    print("MALICIOUS TEST EMAILS (Malicious Probability):")
    print(f"  min: {np.min(mal_probs):.4f}")
    print(f"  max: {np.max(mal_probs):.4f}")
    print(f"  mean: {np.mean(mal_probs):.4f}")
    print(f"  median: {np.median(mal_probs):.4f}")
    
    print("==================================================")
    print("PHASE 9 — THRESHOLD CALIBRATION")
    print("==================================================")
    val_results = reloaded_trainer.predict(val_dataset)
    val_probs_all = torch.nn.functional.softmax(torch.tensor(val_results.predictions), dim=-1).numpy()
    val_malicious_probs = val_probs_all[:, 1]
    val_labels_np = np.array(val_labels)
    
    thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    for t in thresholds:
        val_preds_t = (val_malicious_probs >= t).astype(int)
        acc = accuracy_score(val_labels_np, val_preds_t)
        prec = precision_score(val_labels_np, val_preds_t, zero_division=0)
        rec = recall_score(val_labels_np, val_preds_t, zero_division=0)
        f1 = f1_score(val_labels_np, val_preds_t, zero_division=0)
        cm_t = confusion_matrix(val_labels_np, val_preds_t)
        tn, fp, fn, tp = cm_t.ravel() if cm_t.size == 4 else (0,0,0,0)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        print(f"Threshold: {t:.2f} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | FPR: {fpr:.4f} | FNR: {fnr:.4f}")
        
    print("==================================================")
    print("PHASE 10 — PROMOTE MODEL")
    print("==================================================")
    prod_dir = 'models/bert_phishing'
    if os.path.exists(prod_dir):
        shutil.rmtree(prod_dir)
    shutil.copytree(out_dir, prod_dir)
    print(f"Promoted {out_dir} to {prod_dir}")
    
    # Clean up checkpoint dir
    shutil.rmtree(out_dir)

if __name__ == "__main__":
    main()
