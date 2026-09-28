import os
import shutil

dirs_to_create = [
    'data/raw/ceas',
    'data/raw/enron',
    'data/raw/ling_spam',
    'data/raw/nazario',
    'data/raw/nigerian_fraud',
    'data/raw/spamassassin',
    'data/raw/other',
    'data/inspected',
    'data/intermediate',
    'data/processed'
]

for d in dirs_to_create:
    os.makedirs(d, exist_ok=True)

file_moves = {
    'CEAS_08.csv': 'data/raw/ceas/CEAS_08.csv',
    'Enron.csv': 'data/raw/enron/Enron.csv',
    'Ling.csv': 'data/raw/ling_spam/Ling.csv',
    'Nazario.csv': 'data/raw/nazario/Nazario.csv',
    'Nigerian_Fraud.csv': 'data/raw/nigerian_fraud/Nigerian_Fraud.csv',
    'Phishing_Email.csv': 'data/raw/other/Phishing_Email.csv',
    'SpamAssasin.csv': 'data/raw/spamassassin/SpamAssasin.csv'
}

for src, dest in file_moves.items():
    if os.path.exists(src):
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    else:
        print(f"File {src} not found.")

print("Setup complete.")
