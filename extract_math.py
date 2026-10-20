import docx
import re

doc = docx.Document('05_Reports/Manuscript_IJAI_FINAL_V4.docx')

math_patterns = [
    r'\\\(.*?\\\)',          # \( ... \)
    r'\[\\[a-zA-Z_]+\]',     # [\sigma_t]
    r'\[[a-zA-Z]_[a-zA-Z]\]',# [f_t], [z_t]
    r'\[p < [0-9.]+\]',      # [p < 0.05]
    r'\[H\]',                # [H]
    r'\+3\[\\sigma\]',       # +3[\sigma]
]

for p in doc.paragraphs:
    for pattern in math_patterns:
        matches = re.findall(pattern, p.text)
        if matches:
            print(f"Found: {matches}")
