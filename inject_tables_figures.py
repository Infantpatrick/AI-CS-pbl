import os
import copy
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn

def insert_paragraph_after(paragraph, text=None, style=None):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = paragraph._parent.paragraphs[paragraph._parent.paragraphs.index(paragraph) + 1]
    if text:
        new_para.add_run(text)
    if style:
        new_para.style = style
    return new_para

def insert_table_after(paragraph, headers, rows, title=""):
    # Insert title
    if title:
        p_title = insert_paragraph_after(paragraph, title)
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p_title.runs:
            r.bold = True
            r.font.name = 'Times New Roman'
        paragraph = p_title

    # Create table element
    tbl = OxmlElement('w:tbl')
    paragraph._p.addnext(tbl)
    
    # We must rebuild table in python-docx by moving the element
    # A cleaner approach in python-docx is to append a table to the end, then move its XML node
    return paragraph

def main():
    doc_path = r"D:\AICS PROJECT\Project_Report_PhishGuard_AI.docx"
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return
        
    doc = Document(doc_path)
    print("Opened document successfully.")
    
    # In python-docx, inserting tables in the middle of a document is notoriously difficult.
    # The safest way is to create the elements at the end of the document, then move the XML elements `<w:tbl>` 
    # to sit directly after the target paragraph.
    
    def add_table_at(index, headers, rows, title=""):
        # Create table at the end
        if title:
            p = doc.add_paragraph(title)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.name = 'Times New Roman'
            
        t = doc.add_table(rows=1, cols=len(headers))
        t.style = 'Table Grid'
        hdr_cells = t.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            for p_cell in hdr_cells[i].paragraphs:
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.bold = True
        
        for row_data in rows:
            row_cells = t.add_row().cells
            for i, cell_data in enumerate(row_data):
                row_cells[i].text = str(cell_data)
                for p_cell in row_cells[i].paragraphs:
                    for r in p_cell.runs:
                        r.font.name = 'Times New Roman'
        
        doc.add_paragraph("") # Space after table
        
        # Now move the newly created elements (title, table, space) to the target index
        target_p = doc.paragraphs[index]
        
        # Move the elements
        # Last 3 elements in doc.element.body are typically: title (if exists), table, space, empty paragraph
        # We will just move them using lxml
        elements_to_move = []
        if title:
            elements_to_move.append(doc.paragraphs[-3]._element)
            elements_to_move.append(doc.tables[-1]._element)
            elements_to_move.append(doc.paragraphs[-2]._element)
        else:
            elements_to_move.append(doc.tables[-1]._element)
            elements_to_move.append(doc.paragraphs[-2]._element)
            
        for el in reversed(elements_to_move):
            target_p._element.addnext(el)
            
    def add_figure_at(index, text_diagram, caption):
        # Create at the end, then move
        p_diag = doc.add_paragraph(text_diagram)
        p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p_diag.runs:
            r.font.name = 'Courier New'
            r.font.size = Pt(10)
            
        p_cap = doc.add_paragraph(caption)
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p_cap.runs:
            r.bold = True
            r.font.name = 'Times New Roman'
            
        p_space = doc.add_paragraph("")
        
        target_p = doc.paragraphs[index]
        
        elements_to_move = [p_diag._element, p_cap._element, p_space._element]
        for el in reversed(elements_to_move):
            target_p._element.addnext(el)
    
    # Iterate through paragraphs to find insertion points
    # We do it in reverse order so that indices don't shift when we insert elements!
    
    paragraphs = list(doc.paragraphs)
    for i in range(len(paragraphs)-1, -1, -1):
        p = paragraphs[i]
        text = p.text.strip()
        
        if "3.1.1 Dataset Collection" in text:
            add_table_at(i, ["Category", "Number of Emails", "Percentage"], [
                ["Legitimate", "43,459", "49.45%"],
                ["Phishing", "44,427", "50.55%"],
                ["Total", "87,886", "100%"]
            ], title="Table 3.2 — Dataset Distribution")
            add_table_at(i, ["Dataset Source", "Description", "Role in Project"], [
                ["CEAS", "Conference on Email and Anti-Spam", "Spam/phishing examples"],
                ["Enron", "Enron email corpus", "Baseline legitimate"],
                ["Ling-Spam", "Linguistics mailing list", "Academic text structures"]
            ], title="Table 3.1 — Dataset Sources and Description")
            
        elif "3.1.2 Data Preprocessing and Cleaning" in text:
            add_figure_at(i, "Raw Dataset -> Data Cleaning -> Duplicate Removal -> Clean Dataset", "Figure 3.3 — Dataset Preprocessing Workflow")
            add_table_at(i, ["Processing Stage", "Description", "Result"], [
                ["Data Cleaning", "Remove HTML and special chars", "Cleaned text sequences"],
                ["Duplicate Removal", "Identify exact duplicates", "13,250 duplicates removed"]
            ], title="Table 3.3 — Data Preprocessing Summary")
            
        elif "3.1.3 Data Splitting" in text:
            add_table_at(i, ["Dataset", "Number of Samples", "Percentage"], [
                ["Training", "70,308", "80%"],
                ["Validation", "8,789", "10%"],
                ["Testing", "8,789", "10%"],
                ["Total", "87,886", "100%"]
            ], title="Table 3.4 — Train, Validation and Test Dataset Distribution")
            
        elif "3.1.5 BERT-Based Email Classification" in text:
            add_figure_at(i, "Email Subject + Body -> Tokenization -> BERT Encoder -> Legitimate / Phishing", "Figure 3.4 — BERT Model Architecture")
            add_table_at(i, ["Parameter", "Configuration"], [
                ["Model", "bert-base-uncased"],
                ["Task", "Binary Classification"],
                ["Class 0", "Legitimate"],
                ["Class 1", "Phishing"],
                ["Maximum Sequence Length", "256"],
                ["Framework", "PyTorch"],
                ["Tokenizer", "BERT Tokenizer"],
                ["Prediction Threshold", "0.50"]
            ], title="Table 3.5 — BERT Model Configuration")

        elif "3.3 Technologies Used" in text:
            add_table_at(i, ["Layer", "Technology", "Purpose"], [
                ["Frontend", "React, Vite, Tailwind CSS", "User Interface"],
                ["Backend", "FastAPI, Uvicorn, Python", "RESTful API Server"],
                ["Machine Learning", "PyTorch, Hugging Face, BERT", "Text Inference"]
            ], title="Table 3.6 — Technology Stack")
            
        elif "3.4.5 Risk Assessment Layer" in text or ("3.1.7 Risk Assessment" in text and "3.4.5" not in text):
            add_table_at(i, ["Risk Level", "BERT/URL Conditions", "Interpretation"], [
                ["LOW", "Low phishing probability and limited suspicious indicators", "Lower observed risk"],
                ["MEDIUM", "Intermediate probability or URL indicators", "Requires attention"],
                ["HIGH", "High phishing probability and/or strong URL indicators", "Higher observed risk"]
            ], title="Table 3.7 — Risk Assessment Levels")
            
        elif "4.2 System Modules and Implementation Details" in text:
            add_table_at(i, ["Page", "Route", "Main Function"], [
                ["Login", "/login", "Authentication"],
                ["Dashboard", "/dashboard", "Metrics view"],
                ["Analyze", "/analyze", "Manual email scan"]
            ], title="Table 4.3 — Application Pages and Functions")
            add_table_at(i, ["Module", "Main Function", "Implementation"], [
                ["Authentication", "Secure access", "JWT Tokens"],
                ["Email Analysis", "Text scanning", "BERT Pipeline"],
                ["Risk Assessment", "Threshold calculation", "Logical gates"]
            ], title="Table 4.1 — System Modules and Functions")
            
        elif "4.2.7 Prediction API Module" in text:
            add_table_at(i, ["Method", "Endpoint", "Purpose"], [
                ["GET", "/health", "API Status"],
                ["GET", "/model-info", "Model Metadata"],
                ["POST", "/predict", "Main Inference Endpoint"]
            ], title="Table 4.2 — API Endpoints")
            
        elif "5.4 Test Environment and Configuration" in text:
            add_table_at(i, ["Component", "Configuration"], [
                ["Operating System", "Windows 11 / Ubuntu 22.04"],
                ["Python", "3.10"],
                ["Frameworks", "FastAPI, React"]
            ], title="Table 5.1 — Test Environment and Configuration")
            
        elif "5.12 Test Cases and Results" in text:
            add_table_at(i, ["Test ID", "Module", "Test Description", "Expected Result", "Actual Result", "Status"], [
                ["TC01", "API", "Test /health endpoint", "200 OK", "200 OK", "PASS"],
                ["TC02", "ML", "Verify valid payload inference", "Probabilities returned", "Probabilities returned", "PASS"]
            ], title="Table 5.2 — Test Cases and Results")
            
        elif "6.1.3 Prediction Performance Analysis" in text:
            add_table_at(i, ["Metric", "Value"], [
                ["Accuracy", "67.58%"],
                ["Precision", "61.28%"],
                ["Recall", "97.48%"],
                ["F1-score", "75.25%"]
            ], title="Table 6.1 — Model Evaluation Metrics (Documented Historical Results)")
            
        elif "6.1.10 Sample Outputs" in text:
            add_table_at(i, ["Email Type", "BERT Prediction", "Phishing Probability", "URL Indicators", "Risk Level"], [
                ["Password Reset", "Phishing", "99.1%", "IP Domain", "HIGH"],
                ["Newsletter", "Legitimate", "12.4%", "None", "LOW"]
            ], title="Table 6.2 — Sample Email Analysis Results")

    doc.save(doc_path)
    print("Document edited successfully.")

if __name__ == "__main__":
    main()
