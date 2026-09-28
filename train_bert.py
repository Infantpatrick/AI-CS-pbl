import os
import shutil
import pandas as pd
import numpy as np
import time
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments

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
    print("Loading data...")
    df = pd.read_csv('data/processed/email_phishing_dataset.csv')
    print(f"Total rows: {len(df)}")
    
    # Preprocessing
    # Use canonical format
    # [SUBJECT]\n{subject}\n\n[BODY]\n{body}
    # Ensure missing values are filled
    df['subject'] = df['subject'].fillna("")
    df['body'] = df['body'].fillna("")
    
    texts = []
    labels = []
    for _, row in df.iterrows():
        text = f"[SUBJECT]\n{row['subject']}\n\n[BODY]\n{row['body']}"
        texts.append(text)
        labels.append(int(row['label']))
        
    print(f"Prepared {len(texts)} samples")

    # Split: Train: 70,308 | Validation: 8,789 | Test: 8,789
    # Total: 87886
    # First split off train (70308 / 87886 = 0.8)
    train_texts, temp_texts, train_labels, temp_labels = train_test_split(texts, labels, test_size=(17578/87886), random_state=42)
    # Then split temp into val and test (50% each of 17578 is 8789)
    val_texts, test_texts, val_labels, test_labels = train_test_split(temp_texts, temp_labels, test_size=0.5, random_state=42)
    
    print(f"Train: {len(train_texts)}, Val: {len(val_texts)}, Test: {len(test_texts)}")

    print("Initializing tokenizer...")
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    
    print("Tokenizing...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=256)
    
    train_dataset = PhishingDataset(train_encodings, train_labels)
    val_dataset = PhishingDataset(val_encodings, val_labels)
    test_dataset = PhishingDataset(test_encodings, test_labels)

    print("Loading model...")
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    
    out_dir = 'models/bert_phishing_candidate'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    training_args = TrainingArguments(
        output_dir=out_dir,
        num_train_epochs=1,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_steps=439,
        lr_scheduler_type="linear",
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
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

    print("Starting training...")
    start_time = time.time()
    trainer.train()
    train_time = time.time() - start_time
    print(f"Training completed in {train_time:.2f} seconds.")

    print("Saving candidate model...")
    trainer.save_model(out_dir)
    tokenizer.save_pretrained(out_dir)
    
    # Reload verification
    print("Reloading candidate model for verification...")
    reloaded_model = BertForSequenceClassification.from_pretrained(out_dir)
    if reloaded_model.config.num_labels != 2:
        print(f"ERROR: Model has {reloaded_model.config.num_labels} labels, expected 2.")
        return
        
    print("Model reloaded successfully. Testing inference on sample data...")
    test_emails = [
        # Test 1 - Legitimate
        "[SUBJECT]\nWeekly Project Meeting - Friday at 10:00 AM\n\n[BODY]\nHi Team,\n\nThis is a reminder about our weekly project meeting scheduled for Friday at 10:00 AM. We will discuss the current development progress, pending tasks, and plans for next week.\n\nRegards,\nProject Team",
        # Test 2 - Spam
        "[SUBJECT]\nCongratulations! You Have Won a $5,000 Reward\n\n[BODY]\nCongratulations! Your email address has been selected for a special reward. Claim your $5,000 prize today by completing the confirmation process.",
        # Test 3 - Phishing
        "[SUBJECT]\nURGENT ACTION REQUIRED: Your Account Will Be Permanently Suspended Today\n\n[BODY]\nYour account requires immediate verification. Failure to verify your account today may result in permanent suspension.\n\nPlease verify your account by providing your login credentials, password, card information, CVV and OTP.\n\nVerify now:\nhttp://account-security-verification.example.com/secure-login"
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
            
            print(f"TEST {i+1} PREDICTION: Class={pred_class}, Legit_Prob={probs_np[0]:.4f}, Malicious_Prob={probs_np[1]:.4f}")

    print("Running full test set evaluation...")
    reloaded_trainer = Trainer(
        model=reloaded_model,
        args=TrainingArguments(
            output_dir='tmp_eval',
            per_device_eval_batch_size=16,
        ),
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )
    
    test_results = reloaded_trainer.predict(test_dataset)
    test_metrics = test_results.metrics
    print("Test Metrics:", test_metrics)
    
    preds = test_results.predictions.argmax(-1)
    cm = confusion_matrix(test_labels, preds)
    print("Confusion Matrix:")
    print(cm)
    
    print("Copying model to production path models/bert_phishing...")
    prod_dir = 'models/bert_phishing'
    if os.path.exists(prod_dir):
        shutil.rmtree(prod_dir)
    shutil.copytree(out_dir, prod_dir)
    print("Model successfully promoted to production.")

if __name__ == "__main__":
    main()
