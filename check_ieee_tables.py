import docx

doc = docx.Document('05_Reports/Manuscript_IEEE_FINAL_2026_WORD.docx')
for p in doc.paragraphs:
    text = p.text.strip()
    if text.startswith('TABLE') or text.startswith('Table'):
        print(text)
