import os
from docx import Document

def main():
    doc_path = r"D:\AICS PROJECT\Project_Report_PhishGuard_AI.docx"
    temp_path = r"D:\AICS PROJECT\Project_Report_PhishGuard_AI_temp.docx"
    
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return
        
    doc = Document(doc_path)
    
    seen_tables = set()
    table_titles = [
        "Table 3.1", "Table 3.2", "Table 3.3", "Table 3.4", 
        "Table 3.5", "Table 3.6", "Table 3.7", 
        "Table 4.1", "Table 4.2", "Table 4.3", 
        "Table 5.1", "Table 5.2", 
        "Table 6.1", "Table 6.2"
    ]
    
    body = doc._body._body
    elements_to_remove = []
    
    for element in body.iterchildren():
        if element.tag.endswith('p'):
            from docx.text.paragraph import Paragraph
            p = Paragraph(element, doc)
            text = p.text.strip()
            
            for t_title in table_titles:
                if text.startswith(t_title):
                    if t_title in seen_tables:
                        elements_to_remove.append(element)
                        element._delete_next_table = True
                    else:
                        seen_tables.add(t_title)
                        element._delete_next_table = False
                    break
        
        elif element.tag.endswith('tbl'):
            prev = element.getprevious()
            while prev is not None and not prev.tag.endswith('p'):
                prev = prev.getprevious()
            if prev is not None and getattr(prev, '_delete_next_table', False):
                elements_to_remove.append(element)

    for el in elements_to_remove:
        el.getparent().remove(el)

    doc.save(temp_path)
    print(f"Deduplication complete. Found {len(seen_tables)} unique tables. Saved to temp.")

if __name__ == "__main__":
    main()
