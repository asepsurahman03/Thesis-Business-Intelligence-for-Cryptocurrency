import docx
import re

doc = docx.Document('05_Reports/Manuscript_IJAI_FINAL_V10.docx')

for p in doc.paragraphs:
    if "Table" in p.text or "TABLE" in p.text or "Tabel" in p.text:
        # Just print paragraphs that contain the word Table, particularly captions
        if p.text.strip().startswith("TABLE") or p.text.strip().startswith("Table") or p.text.strip().startswith("TABEL"):
            print(f"Caption Candidate: {p.text}")
