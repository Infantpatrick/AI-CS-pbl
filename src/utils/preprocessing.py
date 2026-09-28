def get_canonical_text(subject, body):
    subject = str(subject).strip() if subject is not None and str(subject) != 'nan' else ""
    body = str(body).strip() if body is not None and str(body) != 'nan' else ""
    return f"[SUBJECT]\n{subject}\n\n[BODY]\n{body}"
