import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_image_after_heading(doc, heading_text, image_path, caption):
    for i, p in enumerate(doc.paragraphs):
        if heading_text in p.text:
            # We must be careful not to duplicate if it's already there
            # Let's insert the image in a new paragraph
            new_p = doc.add_paragraph()
            new_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = new_p.add_run()
            run.add_picture(image_path, width=Inches(5.5))
            
            # Caption
            cap_p = doc.add_paragraph(caption)
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in cap_p.runs:
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
            
            # Move these elements to sit right after the heading
            # or specifically after the explanation paragraph following the heading
            target_element = p._element
            # We want to put it after the explanation paragraph if possible, so move down one block
            if p._element.getnext() is not None and p._element.getnext().tag.endswith('p'):
                target_element = p._element.getnext()
                
            target_element.addnext(cap_p._element)
            target_element.addnext(new_p._element)
            
            return True
    return False

def main():
    doc_path = r"D:\AICS PROJECT\Project_Report_PhishGuard_AI.docx"
    
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return
        
    doc = Document(doc_path)
    
    # We only have actual image files for some of the EDA and Results.
    # We are strictly forbidden from faking screenshots.
    
    img_61 = r"D:\AICS PROJECT\results\eda\class_distribution.png"
    img_63 = r"D:\AICS PROJECT\results\evaluation\confusion_matrix.png"
    
    count = 0
    if os.path.exists(img_61):
        if add_image_after_heading(doc, "6.1.1 Dataset Characteristics", img_61, "Figure 6.1 — Dataset Class Distribution"):
            count += 1
            
    if os.path.exists(img_63):
        if add_image_after_heading(doc, "6.1.3 Prediction Performance Analysis", img_63, "Figure 6.3 — Model Evaluation Results"):
            count += 1
            
    doc.save(doc_path)
    print(f"Successfully injected {count} real images.")

if __name__ == "__main__":
    main()
