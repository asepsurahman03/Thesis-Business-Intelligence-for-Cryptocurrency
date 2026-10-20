import docx

doc = docx.Document('05_Reports/Manuscript_IJAI_FINAL_V2.docx')
with open('dump_v2.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs):
        f.write(f"[{i}] {p.text}\n")
