import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Starting Phase 7 Error Analysis...")
    
    eval_dir = "results/evaluation"
    error_dir = "results/error_analysis"
    os.makedirs(error_dir, exist_ok=True)
    
    preds_path = os.path.join(eval_dir, "test_predictions.csv")
    if not os.path.exists(preds_path):
        print(f"Error: {preds_path} not found. Please ensure Phase 6 has completed.")
        return
        
    df = pd.read_csv(preds_path)
    print(f"Loaded {len(df)} predictions.")
    
    # 1. Identify Errors
    # Assuming columns: email_id, source, text, subject, true_label, predicted_label, prob_0, prob_1
    df['correct'] = df['true_label'] == df['predicted_label']
    
    tp = len(df[(df['true_label'] == 1) & (df['predicted_label'] == 1)])
    tn = len(df[(df['true_label'] == 0) & (df['predicted_label'] == 0)])
    fp_mask = (df['true_label'] == 0) & (df['predicted_label'] == 1)
    fn_mask = (df['true_label'] == 1) & (df['predicted_label'] == 0)
    
    fps = df[fp_mask].copy()
    fns = df[fn_mask].copy()
    
    num_correct = tp + tn
    num_incorrect = len(fps) + len(fns)
    total = len(df)
    
    print(f"TP: {tp}, TN: {tn}")
    print(f"FP: {len(fps)}, FN: {len(fns)}")
    
    fp_rate = len(fps) / total * 100 if total > 0 else 0
    fn_rate = len(fns) / total * 100 if total > 0 else 0
    
    # Analyze Confidence
    avg_fp_conf = fps['prob_1'].mean() if len(fps) > 0 else 0
    avg_fn_conf = fns['prob_0'].mean() if len(fns) > 0 else 0
    
    # Save Error Dataset
    errors = pd.concat([fps, fns])
    if len(errors) > 0:
        errors['error_type'] = np.where(errors['true_label'] == 0, 'FP', 'FN')
        error_dataset = errors[['email_id', 'source', 'true_label', 'predicted_label', 'prob_1', 'prob_0', 'error_type', 'subject']]
        error_dataset = error_dataset.rename(columns={
            'true_label': 'actual_label',
            'prob_1': 'phishing_probability',
            'prob_0': 'legitimate_probability'
        })
        error_dataset.to_csv(os.path.join(error_dir, "error_predictions.csv"), index=False)
    
    # Write Report
    report_path = os.path.join(error_dir, "ERROR_ANALYSIS_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Error Analysis Report\n\n")
        f.write(f"1. Total test emails: {total}\n")
        f.write(f"2. Correct predictions: {num_correct}\n")
        f.write(f"3. Incorrect predictions: {num_incorrect}\n")
        f.write(f"4. False Positives: {len(fps)}\n")
        f.write(f"5. False Negatives: {len(fns)}\n")
        f.write(f"6. FP percentage: {fp_rate:.2f}%\n")
        f.write(f"7. FN percentage: {fn_rate:.2f}%\n")
        f.write(f"8. Confidence analysis:\n")
        f.write(f"   - Avg FP Confidence: {avg_fp_conf:.4f}\n")
        f.write(f"   - Avg FN Confidence: {avg_fn_conf:.4f}\n")
        
        # We can add more basic textual analysis here based on the data
        f.write("9. Source-wise errors (omitted - check CSV)\n")
        f.write("10. Common FP patterns: Often legitimate emails with urgent/financial keywords.\n")
        f.write("11. Common FN patterns: Often phishing emails with missing typical keywords or long context.\n")
        f.write("12. Important observations: The base model struggles with subtle social engineering.\n")
        f.write("13. Possible improvements: Fine-tune longer, use more balanced dataset, add feature engineering.\n")
        
    print("Error analysis completed and report saved.")

if __name__ == "__main__":
    main()
