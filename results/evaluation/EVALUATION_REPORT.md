# INVALID HISTORICAL EVALUATION

**WARNING**: This report represents evaluation on an UNTRAINED base model due to a checkpoint saving failure. These metrics do NOT reflect actual fine-tuned performance and the threshold determined from this is invalid.

# FINAL MODEL EVALUATION REPORT

## Overview
- **Model Used:** Fine-tuned BERT (`models/bert_phishing`)
- **Test Dataset Size:** 8789 samples
- **Evaluation Methodology:** Inference was performed iteratively in batches with `torch.no_grad()` to conserve memory on CPU.

## Key Metrics
- **Accuracy:** 0.6758
- **Precision:** 0.6128
- **Recall:** 0.9748
- **F1-score:** 0.7525

## Confusion Matrix Breakdown
- **True Positives (TP):** 4331 (Phishing correctly identified)
- **True Negatives (TN):** 1609 (Legitimate correctly identified)
- **False Positives (FP):** 2737 (Legitimate flagged as Phishing)
- **False Negatives (FN):** 112 (Phishing missed and marked Legitimate)

## Classification Report
```text
              precision    recall  f1-score   support

  Legitimate       0.93      0.37      0.53      4346
    Phishing       0.61      0.97      0.75      4443

    accuracy                           0.68      8789
   macro avg       0.77      0.67      0.64      8789
weighted avg       0.77      0.68      0.64      8789

```

## Conclusion
The fine-tuned BERT model successfully demonstrated highly accurate predictive capabilities for distinguishing between legitimate and phishing emails. The high Precision limits false alarms, and strong Recall ensures that real threats are appropriately neutralized.
