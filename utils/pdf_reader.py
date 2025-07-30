# pdf_reader.py
import fitz  # PyMuPDF
import re
import os

def extract_pdf_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    importance_rank = 1

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            if re.match(r"^\d{0,2}\.?[A-Z][A-Za-z\s\-:]{3,}$", line.strip()):
                sections.append({
                    "document": os.path.basename(pdf_path),
                    "page_number": page_num + 1,
                    "section_title": line.strip(),
                    "importance_rank": importance_rank,
                    "refined_text": page.get_text().strip()
                })
                importance_rank += 1

    doc.close()
    return sections
    