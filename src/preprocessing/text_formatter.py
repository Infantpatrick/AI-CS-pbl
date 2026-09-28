def format_bert_text(subject: str, body: str) -> str:
    """
    Shared preprocessing function to format email subject and body into the
    canonical BERT input string. Must be used consistently across training,
    evaluation, and production.
    """
    # Ensure strings and handle missing values
    subj = str(subject) if subject and str(subject) != 'nan' else ''
    bdy = str(body) if body and str(body) != 'nan' else ''
    
    return f"[SUBJECT]\n{subj}\n\n[BODY]\n{bdy}"
