import os
import re
from docx import Document

def main():
    doc_path = r"D:\AICS PROJECT\Project_Report_PhishGuard_AI.docx"
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return
        
    doc = Document(doc_path)
    
    seen_tables = set()
    seen_figures = set()
    
    table_titles = [
        "Table 3.1", "Table 3.2", "Table 3.3", "Table 3.4", 
        "Table 3.5", "Table 3.6", "Table 3.7", 
        "Table 4.1", "Table 4.2", "Table 4.3", 
        "Table 5.1", "Table 5.2", 
        "Table 6.1", "Table 6.2"
    ]
    
    figure_titles = [
        "Figure 3.1", "Figure 3.2", "Figure 3.3", "Figure 3.4", 
        "Figure 3.5", "Figure 3.6", "Figure 3.7",
        "Figure 4.1", "Figure 4.2", "Figure 4.3", "Figure 4.4",
        "Figure 4.5", "Figure 4.6", "Figure 4.7", "Figure 4.8",
        "Figure 4.9", "Figure 4.10", "Figure 4.11", "Figure 4.12",
        "Figure 5.1", "Figure 5.2", "Figure 5.3",
        "Figure 6.1", "Figure 6.2", "Figure 6.3",
        "Figure 6.4", "Figure 6.5", "Figure 6.6"
    ]
    
    body = doc._body._body
    elements_to_remove = []
    
    for element in body.iterchildren():
        if element.tag.endswith('p'):
            from docx.text.paragraph import Paragraph
            p = Paragraph(element, doc)
            text = p.text.strip()
            
            # 1. Fix duplicated paragraphs generated in v3
            if "(Paragraph " in text:
                if "(Paragraph 1)" in text:
                    # Remove the suffix for the first paragraph to make it normal
                    for run in p.runs:
                        if "(Paragraph 1)" in run.text:
                            run.text = run.text.replace("(Paragraph 1)", "").strip()
                else:
                    # Delete duplicated paragraphs like (Paragraph 2), (Paragraph 3), etc.
                    elements_to_remove.append(element)
                    continue
            
            # 2. Fix duplicated Tables
            is_table_caption = False
            for t_title in table_titles:
                if text.startswith(t_title):
                    is_table_caption = True
                    if t_title in seen_tables:
                        elements_to_remove.append(element)
                        element._delete_next_table = True
                    else:
                        seen_tables.add(t_title)
                        element._delete_next_table = False
                    break
            
            # 3. Fix duplicated Figures
            if not is_table_caption:
                for f_title in figure_titles:
                    if text.startswith(f_title):
                        if f_title in seen_figures:
                            elements_to_remove.append(element)
                            # Figures usually have an image inside a paragraph or nearby.
                            # We will mark to delete the previous paragraph (which often contains the image)
                            # or just remove this duplicate caption. 
                            # Since figures were inserted as: Image/Diagram -> Caption -> Space
                            # It's safer to just remove the caption if we can't reliably find the image.
                            # But wait, my script added diagram paragraph THEN caption paragraph.
                            # So the previous paragraph is the diagram!
                            prev = element.getprevious()
                            if prev is not None and prev.tag.endswith('p'):
                                elements_to_remove.append(prev)
                        else:
                            seen_figures.add(f_title)
                        break
        
        elif element.tag.endswith('tbl'):
            # Delete table if the preceding caption was marked as duplicate
            prev = element.getprevious()
            while prev is not None and not prev.tag.endswith('p'):
                prev = prev.getprevious()
            if prev is not None and getattr(prev, '_delete_next_table', False):
                elements_to_remove.append(element)

    # Remove all marked elements
    for el in set(elements_to_remove): # use set to avoid double removal
        try:
            el.getparent().remove(el)
        except Exception:
            pass # Already removed

    # Validate final counts
    print(f"Unique tables retained: {len(seen_tables)} (Target: 14)")
    print(f"Unique figures retained: {len(seen_figures)}")
    
    doc.save(doc_path)
    print("Document successfully repaired and saved.")

if __name__ == "__main__":
    main()
