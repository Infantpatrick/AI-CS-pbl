with open('results/EDA_REPORT.md', 'a') as f:
    f.write("\n\n## Phase 2.5: EDA Validation\n\n")
    f.write("### 1. Missing Values Analysis\n")
    f.write("The 6,480 total missing values are distributed as follows:\n")
    f.write("- **Subject**: 6,474 missing values (7.37%)\n")
    f.write("- **Body**: 6 missing values (0.01%)\n")
    f.write("- **Total Emails Affected**: 6,479 emails\n\n")
    
    f.write("### 2. HTML Detection\n")
    f.write("The EDA reported **0 HTML emails** because HTML tags were proactively removed during the Phase 1 cleaning process. The `clean.py` script utilized `html.unescape` and regex (`<[^>]+>`) to strip all tags like `<html>`, `<body>`, `<a>`, and `<table>` from the subjects and bodies before the dataset was saved to `data/processed/`.\n\n")
    
    f.write("### 3. Final Validation\n")
    f.write("- **Total emails**: 87,886\n")
    f.write("- **Legitimate**: 43,459\n")
    f.write("- **Phishing**: 44,427\n")
    f.write("- **Duplicates**: 0\n")
    f.write("- **Invalid labels**: 0\n")
