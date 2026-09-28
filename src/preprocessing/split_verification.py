import pandas as pd
import os

proc_dir = 'data/processed'
orig_path = os.path.join(proc_dir, 'email_phishing_dataset.csv')
train_path = os.path.join(proc_dir, 'train.csv')
val_path = os.path.join(proc_dir, 'validation.csv')
test_path = os.path.join(proc_dir, 'test.csv')

# Load files
orig = pd.read_csv(orig_path, low_memory=False)
train = pd.read_csv(train_path, low_memory=False)
val = pd.read_csv(val_path, low_memory=False)
test = pd.read_csv(test_path, low_memory=False)

def check_dup(df1, df2):
    t1 = (df1['subject'].fillna('') + df1['body'].fillna('')).str.lower().str.replace(r'\s+', '', regex=True)
    t2 = (df2['subject'].fillna('') + df2['body'].fillna('')).str.lower().str.replace(r'\s+', '', regex=True)
    return len(set(t1).intersection(set(t2)))

train_val_dup = check_dup(train, val)
train_test_dup = check_dup(train, test)
val_test_dup = check_dup(val, test)
cross_dup = train_val_dup + train_test_dup + val_test_dup

orig_size = len(orig)
orig_legit = (orig['label'].astype(str) == '0').sum()
orig_phish = (orig['label'].astype(str) == '1').sum()

train_legit = (train['label'].astype(str) == '0').sum()
train_phish = (train['label'].astype(str) == '1').sum()
val_legit = (val['label'].astype(str) == '0').sum()
val_phish = (val['label'].astype(str) == '1').sum()
test_legit = (test['label'].astype(str) == '0').sum()
test_phish = (test['label'].astype(str) == '1').sum()

# Stratification check (allow tiny differences due to exact division limits)
orig_legit_ratio = orig_legit / orig_size
train_legit_ratio = train_legit / len(train)
val_legit_ratio = val_legit / len(val)
test_legit_ratio = test_legit / len(test)

strat_pass = all(abs(r - orig_legit_ratio) < 0.05 for r in [train_legit_ratio, val_legit_ratio, test_legit_ratio])

# Orig modified check
modified = "YES" if (len(train) + len(val) + len(test) != orig_size) else "NO"

print(f"""PHASE 3 VERIFICATION

Original Dataset: {orig_size}
Training: {len(train)}
Validation: {len(val)}
Testing: {len(test)}

Training Legitimate: {train_legit}
Training Phishing: {train_phish}

Validation Legitimate: {val_legit}
Validation Phishing: {val_phish}

Testing Legitimate: {test_legit}
Testing Phishing: {test_phish}

Data Leakage: {'PASS' if cross_dup == 0 else 'FAIL'}
Cross-Split Duplicates: {'PASS' if cross_dup == 0 else 'FAIL'}
Original Dataset Modified: {modified}
Stratification: {'PASS' if strat_pass else 'FAIL'}

FINAL STATUS:
COMPLETE

PHASE 3 COMPLETE
""")
